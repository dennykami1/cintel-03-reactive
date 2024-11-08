from shiny import App, render, ui, reactive
import palmerpenguins

# Load the penguins dataset
penguins = palmerpenguins.load_penguins()

app_ui = ui.page_fluid(
    ui.card(
        ui.h5(
            "Filter Data by Year or Select All Years with the Checkbox:",
            ui.hr(style="border-top: 4px solid #0fa3b1; margin-top: 5px; margin-bottom: 0px;")  # Controls the space around the line
        ),
        ui.div(
            ui.input_checkbox_group(
                "species_filter", 
                "Select Species to Filter Data:", 
                choices=["Adelie", "Chinstrap", "Gentoo"], 
                selected=["Adelie", "Chinstrap", "Gentoo"]
            ),
            style="background-color: transparent; margin-top: 15; margin-bottom: 10px;"
        ),
        ui.div(
            ui.input_checkbox_group(
                "sex_filter", 
                "Select Sex to Filter Data:", 
                choices=["male", "female"], 
                selected=["male", "female"],
            ),
            style="background-color: transparent; margin-top: 15; margin-bottom: 2px;"
        ),
        ui.hr(style="border-top: 2px solid #0fa3b1; margin-top: 1px; margin-bottom: 1px;"),
        ui.div(
            ui.input_checkbox("all_years", "Check to Show data from All Years", True),
            style="background-color: transparent; margin-top: 15; margin-bottom: 10px;"
        ),
        ui.div(
            ui.input_slider("n", "Select Year:", 2007, 2009, 2007),
            style="background-color: transparent;"
        ),
        style="background-color: #f9f7f3; padding: 15px; border-radius: 8px;"
    ),
    
    # Display filtered data as a data frame
    ui.card(
        ui.div(
            ui.output_data_frame("grid"),
            style="background-color: transparent;"
        ),
        style="background-color: #ecf8f8; padding: 15px; border-radius: 8px;"
    ),
)

def server(input, output, session):
    # Observe the "Show All Years" checkbox to update the slider dynamically
    @reactive.Effect
    def toggle_slider():
        if input.all_years():
            # If "Show All Years" is checked, lock the slider to a single value
            ui.update_slider("n", value=2007, min=2007, max=2007, label="All Years Selected")
            ui.update_checkbox("all_years", label="Uncheck to Filter Data by Year using Slider")
        else:
            # Restore the slider's full range if "Show All Years" is unchecked
            ui.update_slider("n", min=2007, max=2009, label="Select Year:")
            ui.update_checkbox("all_years", label="Check to Show data from All Years")
    
    # Reactive function to filter data based on species, sex, year, and "All Years" checkbox
    @reactive.Calc
    def filtered_data():
        # Start by filtering based on selected species
        filtered = penguins[penguins['species'].isin(input.species_filter())]
        
        # Apply sex filter if selected
        filtered = filtered[filtered['sex'].isin(input.sex_filter())]
        
        # Apply year filter if "Show All Years" is unchecked
        if not input.all_years():
            filtered = filtered[filtered['year'] == int(input.n())]
        
        return filtered
    
    
    # Render the filtered data as a data frame
    @output
    @render.data_frame
    def grid():
        return filtered_data()

app = App(app_ui, server)
