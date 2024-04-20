"""
Purpose: Provide user interaction options for MT Cars dataset.

IDs must be unique. They are capitalized in this app for clarity (not typical).
The IDs are case-sensitive and must match the server code exactly.
Preface IDs with the dataset name to avoid naming conflicts.

""" 
from shiny import ui

# Define the UI inputs and include our new selection options

def get_tests_inputs():
    return ui.panel_sidebar(
        ui.tags.section(
            ui.h3("Filter Results"),
            ui.input_checkbox_group(
                id="EVENT_DISPLAY_SELECT",
                label="Choose the events to show results for",
                choices=["100m", "200m", "400m", "800m", "1500m", "1600m", "3200m", "5000m", "10000m", "Shot Put", "Discus", "Javelin", "Long Jump", "High Jump", "Triple Jump", "Pole Vault"],
                selected="100m",
            ),
        ),
        ui.tags.hr(),
            ui.tags.section(
            ui.input_checkbox_group(
                id="DIVISION_DISPLAY_SELECT",
                label="Choose the divisions to show results for",
                choices=["Kansas 1A", "Kansas 3A", "Kansas 6A", "NAIA", "NCAA D-I", "NCAA D-II", "NCAA D-III", "World"],
                selected="World",
            ),
        ),
        ui.tags.hr(),
            ui.tags.section(
            ui.input_checkbox_group(
                id="SEX_DISPLAY_SELECT",
                label="Choose to show results for",
                choices=["Men", "Women"],
                selected="Women",
            ),
        ),
        ui.tags.hr(),
            ui.tags.section(
            ui.input_select(
                id="ZEROSHIFT_RESULTS",
                label="Choose to display results with or without zero shift",
                choices=["Unshifted", "Shifted"],
                selected="Unshifted",
            ),
        ),
        ui.tags.hr(),
        ui.tags.section(
            ui.h3("Notes"),
            ui.tags.p("Have fun with it. If you have requests for more features, send a Github pull request."),
            ui.tags.p("Yes, pole vault is broken. I don't know why and I don't have time to fix it."),
            ui.tags.p("Description of each field in the table:"),
            ui.tags.ul(
                ui.tags.li("Sex: Men or Women"),
                ui.tags.li("Division: Level of Competition"),
                ui.tags.li("Year: Self explanatory"),
                ui.tags.li("Points: World Athletics scoring calculation"),
            ),
            ui.output_table("tests_table"),
        ),
        ui.tags.hr(),
        ui.p("🕒 Please be patient. Outputs may take a few seconds to load."),
        ui.tags.hr(),
    )
