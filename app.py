from shiny import App, Inputs, Outputs, Session, ui, render
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd  # Import pandas here
from shinywidgets import output_widget, render_widget
import shinyswatch
from palmerpenguins import load_penguins 
import seaborn as sns
from shiny import reactive
import ipyleaflet as ipyl

# Load the Palmer Penguins dataset
penguins = load_penguins()  # Correctly load the dataset

# Define a dictionary for display names mapped to column names
column_choices = {
    "Flipper Length (mm)": "flipper_length_mm",
    "Body Mass (g)": "body_mass_g",
    "Bill Length (mm)": "bill_length_mm",
    "Bill Depth (mm)": "bill_depth_mm"
}

# Define custom colors for each species
color_map = {
    "Adelie": "#1f77b4",  # Blue
    "Chinstrap": "#f75c03",  # Orange
    "Gentoo": "#801a86"  # Purple
}

# Coordinates for the islands
island_coordinates = {
    "Biscoe Island": (-65.0, -64.0),
    "Dream Island": (-64.0, -62.0),
    "Torgersen Island": (-64.0, -63.0)
}

# Extract the display names and use them as choices
display_names = list(column_choices.keys())

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(""" 
            .title-box {
                background-color: #f49e4c; /* Title box color */
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
                font-family: 'Arial', sans-serif;
                font-size: 15px;
                color: #111111;
                margin-bottom: 5px;
                border-radius: 12px;
            }
            .sidebar-custom {
                background-color: #8ecae6; /* Sidebar background color */
                padding: 35px;
                border-radius: 12px;
                border: 1px solid #edf6f9;
            }
            .custom-border-card {
                border: 12px solid #8ecae6; /* Border color for outer cards */
                border-radius: 12px;
                padding: 0; /* No padding in the card to avoid gap */
                margin-bottom: 10px;
            }
            .card-header {
                margin: -3px 0 0 0;
                padding: 10px; /* Maintain your padding */
                background-color: #8ecae6; /* Header background color */
                color: #14213d; /* Header text color */
                border-top: 3px solid #8ecae6; /* Header top border color */
                border-bottom: 3px solid #8ecae6; /* Header bottom border color */
            }
        """)
    ),
    ui.card(
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.h1("Side Bar"),
                    ui.hr(style="border-top: 4px solid #f75c03;"),
                    
                    #Seaborn Sidebar
                    ui.h3("Seaborn Histogram Inputs"),
                    ui.input_slider("n", "Seaborn Bin Count", 1, 50, 25),
                    ui.input_selectize(
                        "selected_attribute",  # Name of the input
                        "Select a column for X-axis:",  # Label for the input
                        choices=display_names,  # Use display names in dropdown
                        selected="Body Mass (g)"  # Default selection
                    ),
                    ui.input_checkbox_group(
                        "multi_choice_input",
                        "Select One or More Penguin Species to Display:",
                        choices=["Adelie", "Chinstrap", "Gentoo"],
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False
                    ),
                    ui.input_checkbox(
                        "show_all",
                        "Show Selected Species without Overlay"
                    ),
                    
                    ui.hr(style="border-top: 4px solid #f75c03;"),
                            
                    #Plotly Sidebar
                    ui.h3("Plotly Histogram Inputs"),  # Heading 2 for the histogram card title
                    ui.input_selectize(
                        "x_column", 
                        "Select a column for X-axis:", 
                        choices=display_names,  # Display names in dropdown
                        selected="Body Mass (g)"
                    ),
                    ui.input_numeric("numeric", "Number of bins", 20, min=1, max=100),  
                    ui.input_checkbox_group( 
                        "multi_choice_PlotlyH",
                        "Select One or More Penguin Species to Display:",
                        choices=["Adelie", "Chinstrap", "Gentoo"],
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False
                    ),
                    ui.input_checkbox(
                        "show_all_PlotlyH",
                        "Show Selected Species without Overlay"
                    ),
                    ui.input_checkbox(
                        "single_color",
                        "Display Selected Species in a Single Color"
                    ),
                    
                    ui.hr(style="border-top: 4px solid #f75c03;"),


                    ui.h3("Plotly Scatter Plot Inputs"),  # Heading 2 for the scatter plot card title
                    ui.input_selectize(
                        "x_column_scatter", 
                        "Select a column for X-axis:", 
                        choices=display_names,  # Display names in dropdown
                        selected="Body Mass (g)"
                    ),
                    ui.input_selectize(
                        "y_column_scatter", 
                        "Select a column for Y-axis:", 
                        choices=display_names,  # Display names in dropdown
                        selected="Flipper Length (mm)"
                    ),
                    ui.input_checkbox_group( 
                        "species_input",
                        "Select One or More Penguin Species to Display:",
                        choices=["Adelie", "Chinstrap", "Gentoo"],
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False
                    ),
                    ui.hr(style="border-top: 4px solid #f75c03;"),
                    ui.a("GitHub", href="https://github.com/dennykami1/cintel-02-data", target="_blank"),
                    class_="sidebar-custom"  # Apply custom sidebar class              
                ),
            ),
            ui.div(
                ui.h2("Exploring Interactive UI, Plotly, and Seaborn with Palmer Penguins Data"),
                class_="title-box"
            ),
            ui.page_fillable(
                ui.card(
                    ui.card_header("Interactive Histograms in PyShiny with Seaborn and Plotly", style="background-color: #8ecae6; color: #14213d;"),
                    ui.layout_columns(
                        ui.card(
                            ui.h2("Seaborn Histogram"),
                            ui.output_plot("plot"),     
                        ),
                        ui.card(
                            ui.h2("Plotly Histogram"),
                            output_widget("penguins_histogram"),  # Output widget for histogram
                            full_screen=True  # Make inner card full-screen width
                        )
                    ),
                    class_="custom-border-card"  # Apply custom border class to this card only
                ),
                full_screen=True  # Make inner card full-screen width
            ),
            ui.card(
                ui.card_header("Scatter Plot using Plotly & Interactive Map using ipyleaflet", style="background-color: #8ecae6; color: #14213d;"),
                ui.layout_columns(
                    ui.card(
                        ui.h2("Plotly Scatter Plot"),
                        output_widget("penguins_scatter_plot"),
                    ),
                    ui.card(
                        ui.input_select("center", "Select Island", choices=list(island_coordinates.keys())),
                        output_widget("map"),             
                        full_screen=True,  # Make inner card full-screen width
                    )
                ),     
                class_="custom-border-card"  # Apply custom border class to this card only
            ), 
            ui.card(
                ui.card_header("Palmer Penguins Data Frame & Data Grid", style="background-color: #8ecae6; color: #14213d;"),
                ui.layout_columns(
                    ui.card(
                        ui.column(
                            11,
                            ui.h2("Data Frame"),
                            ui.output_data_frame("penguins_df")
                        )
                    ),
                    ui.card(
                        ui.column(
                            11,
                            ui.h2("Data Table"),
                            ui.output_data_frame("penguins_dt")
                        )
                    )
                ),
                class_="custom-border-card",  # Apply custom border class to this card only
                full_screen=True  # Outer card full-screen width
            ),
            ui.div(
                ui.h4("Author: Kami Denny"),
                class_="title-box"
            ),
        ),
        full_screen=True,  # Outer card full-screen width
        style="padding: 20px;"
    ),
    theme=shinyswatch.theme.lumen
)

def server(input, output, session):

    # Create the map widget globally so it can be accessed in reactive updates
    imagery_map = ipyl.Map(zoom=10, center=(-64.5, -63.0))
    
    # Add satellite imagery layer
    imagery_layer = ipyl.TileLayer(
        url='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attribution='&copy; <a href="https://www.esri.com/">ESRI</a>',
        name='Satellite Imagery'
    )
    imagery_map.add_layer(imagery_layer)
    
    # Create a penguin icon
    penguin_icon_url = "https://cdn.pixabay.com/photo/2024/03/27/17/35/penguin-8659564_1280.png"
    penguin_icon = ipyl.Icon(icon_url=penguin_icon_url, icon_size=(45, 45))
    
    # Add markers for each island
    for island, coords in island_coordinates.items():
        penguin_marker = ipyl.Marker(location=coords, icon=penguin_icon, draggable=False)
        imagery_map.add_layer(penguin_marker)
    
    # Output the map widget
    @output
    @render_widget
    def map():
        return imagery_map

    # Reactive effect to update the map center when an island is selected
    @reactive.Effect
    def _():
        selected_island = input.center()
        if selected_island in island_coordinates:
            imagery_map.center = island_coordinates[selected_island]
            imagery_map.zoom = 13  # Adjust zoom level for better visibility
    
    @render.plot(alt="A Seaborn histogram on penguin data.")  
    def plot():
        selected_display_name = input.selected_attribute()
        selected_column = column_choices[selected_display_name]
        selected_species = input.multi_choice_input()

        # Ensure at least one species is selected
        if not selected_species:
            raise ValueError("Please select at least one species.")

        # Filter penguins DataFrame based on selected species
        filtered_penguins = penguins[penguins['species'].isin(selected_species)]

        # Determine overlay based on checkbox
        multiple_mode = "layer" if not input.show_all() else "stack"

        # Plotting with the selected settings
        if selected_column in filtered_penguins.columns:
            if pd.api.types.is_numeric_dtype(filtered_penguins[selected_column]):
                ax = sns.histplot(
                    data=filtered_penguins, x=selected_column, bins=input.n(),
                    hue="species" if not input.show_all() else None,
                    palette=color_map, multiple=multiple_mode, kde=True
                )
                ax.set_title("Palmer Penguins")
                ax.set_xlabel(selected_display_name)
                ax.set_ylabel("Count")
            else:
                ax = sns.histplot(
                    data=filtered_penguins, x="body_mass_g", bins=input.n(),
                    hue="species" if not input.show_all() else None,
                    palette=color_map, multiple=multiple_mode, kde=True
                )
                ax.set_title("Palmer Penguins")
                ax.set_xlabel("Body Mass (g)")
                ax.set_ylabel("Count")
                ax.text(0.5, 0.5, 'Selected column is not numeric.',
                        horizontalalignment='center', verticalalignment='center',
                        transform=ax.transAxes, fontsize=12, color='purple')
        else:
            ax = sns.histplot(
                data=filtered_penguins, x="body_mass_g", bins=input.n(),
                hue="species" if not input.show_all() else None,
                palette=color_map, multiple=multiple_mode, kde=True
            )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Body Mass (g)")
            ax.set_ylabel("Count")
            ax.text(0.5, 0.5, 'Column not found!',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12, color='purple')
        
        return ax
    
    @render_widget 
    def penguins_histogram():  
        # Map the display name back to the actual column name
        x_column_name = column_choices[input.x_column()]

        # Filter the penguins dataset based on selected species
        selected_species = input.multi_choice_PlotlyH()
        filtered_penguins = penguins[penguins["species"].isin(selected_species)]

        # Define color for single color option
        single_color = "#636EFA"  # Default color (you can change this)

        # Check if the user wants to show all species without overlay
        if input.show_all_PlotlyH():
            # Create histogram plot without overlay for selected species
            histogram = px.histogram(
                data_frame=filtered_penguins,
                x=x_column_name,  # Dynamic x-axis based on actual column name
                nbins=input.numeric(),
                color="species" if not input.single_color() else None,  # Conditional color
                barmode="group",  # Group the bars side by side
                color_discrete_map=color_map if not input.single_color() else {"All": single_color}  # Use the custom color map or single color
            ).update_layout(
                title={"text": f"Penguin {input.x_column()} Distribution by Species", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.x_column(),
            )
        else:
            # Create histogram plot based on selected x-axis column with species overlay and custom colors
            histogram = px.histogram(
                data_frame=filtered_penguins,
                x=x_column_name,  # Dynamic x-axis based on actual column name
                nbins=input.numeric(),
                color="species" if not input.single_color() else None,  # Conditional color
                barmode="overlay",  # Overlay the bars instead of stacking
                color_discrete_map=color_map if not input.single_color() else {"All": single_color}  # Use the custom color map or single color
            ).update_layout(
                title={"text": f"Penguin {input.x_column()} Distribution by Species", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.x_column(),
            )

        return histogram 
    
    @render_widget 
    def penguins_scatter_plot():  
        # Map the display names back to the actual column names
        x_column_name = column_choices[input.x_column_scatter()]
        y_column_name = column_choices[input.y_column_scatter()]

        # Filter the penguins dataset based on selected species
        selected_species = input.species_input()
        filtered_penguins = penguins[penguins["species"].isin(selected_species)]

        # Create scatter plot
        scatterplot = px.scatter(
            data_frame=filtered_penguins,
            x=x_column_name,  # X-axis based on user selection
            y=y_column_name,  # Y-axis based on user selection
            color="species",  # Color points by species
            color_discrete_map=color_map,  # Use the custom color map
            title=f"{input.x_column_scatter()} vs {input.y_column_scatter()}",
            labels={x_column_name: input.x_column_scatter(), y_column_name: input.y_column_scatter()}  # Custom labels for axes
        ).update_layout(
            title={"text": f"{input.x_column_scatter()} vs {input.y_column_scatter()}", "x": 0.5},
            yaxis_title=input.y_column_scatter(),
            xaxis_title=input.x_column_scatter(),
        )

        return scatterplot

    @output
    @render.data_frame
    def penguins_df():
        return render.DataGrid(penguins)

    @output
    @render.data_frame  
    def penguins_dt():
        return render.DataTable(penguins) 

app = App(app_ui, server, debug=True)
