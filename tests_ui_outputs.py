"""
Purpose: Display output for MT Cars dataset.

@imports shiny.ui as ui 
@imports shinywidgets.output_widget for interactive charts
"""
from shiny import ui
from shinywidgets import output_widget


def get_tests_outputs():
    return ui.panel_main(
        ui.h2("Main Panel with Reactive Output"),
        ui.tags.hr(),
        ui.tags.section(
            ui.output_text("result_string"), #Pulls from 'server' file
            ui.tags.br(),
            output_widget("result_chart"),
            ui.tags.br(),
            ui.output_ui("result_table"),
            ui.tags.br(),
        ),
    )
