from shiny import App, render, ui, reactive
import palmerpenguins

# Load the penguins dataset
penguins = palmerpenguins.load_penguins()

app_ui = ui.page_fluid(
    ui.h2("Penguins Data Year and Species Filter", style="background-color:blue; color:white;"),
    
    # Checkbox for toggling "Show All Years"
    ui.input_checkbox("all_years", "Show All Years", False),
    
    # Slider for selecting a specific year
    ui.input_slider("n", "Select Year:", 2007, 2009, 2007),
    
    # Multi-checkbox for filtering by species
    ui.input_checkbox_group(
        "species_filter", 
        "Select Species:", 
        choices=["Adelie", "Chinstrap", "Gentoo"], 
        selected=["Adelie", "Chinstrap", "Gentoo"]
    ),
    
    # Display filtered data as a data frame
    ui.output_data_frame("grid")
)

def server(input, output, session):
    # Observe the "Show All Years" checkbox to update the slider dynamically
    @reactive.Effect
    def toggle_slider():
        if input.all_years():
            # If "Show All Years" is checked, lock the slider to a single value
            ui.update_slider("n", value=2007, min=2007, max=2007, label="All Years Selected")
        else:
            # Restore the slider's full range if "Show All Years" is unchecked
            ui.update_slider("n", min=2007, max=2009, label="Select Year:")
    
    # Reactive function to filter data based on species, year, and "All Years" checkbox
    @reactive.Calc
    def filtered_data():
        # Start by filtering based on selected species
        filtered = penguins[penguins['species'].isin(input.species_filter())]
        
        # Apply year filter if "Show All Years" is unchecked
        if not input.all_years():
            filtered = filtered[filtered['year'] == int(input.n())]
        
        return filtered
    
    # Render the filtered data as text
    @output
    @render.text
    def filtered_txt():
        return filtered_data().to_string()
    
    # Render the filtered data as a data frame
    @output
    @render.data_frame
    def grid():
        return filtered_data()

app = App(app_ui, server)
