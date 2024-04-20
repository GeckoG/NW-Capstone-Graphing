""" 
Purpose: Provide continuous and reactive output for the MT Cars dataset.

- Use inputs from the UI Sidebar to filter the dataset.
- Update reactive outputs in the UI Main Panel.

Matching the IDs in the UI Sidebar and function/output names in the UI Main Panel
to this server code is critical. They are case sensitive and must match exactly.

------------------------------------
Important Concept - Variable Scope
------------------------------------
In Python, the scope of a variable refers to where in the code that variable 
can be accessed and used. 

Variables defined outside of functions or blocks have global scope 
and can be used anywhere in the file. 

Variables defined inside a function or block have local scope 
and can only be used within that specific function or block.

------------------------------------
Important Concept - Reactivity
------------------------------
Reactive Effects only have "side effects" (they set reactive values, but don't return anything directly).
Reactive Calcs return a value (they can also set reactive values).
If a reactive.Effect depends on inputs, you must add them using the
reactive.event decorator (otherwise, the function won't be triggered).
"""

# Standard Library
from pathlib import Path

# External Libraries
import matplotlib.pyplot as plt
import pandas as pd
from plotnine import aes, geom_point, ggplot, ggtitle
import plotly.express as px
import plotly.graph_objects as go
from shiny import render, reactive
from shinywidgets import render_widget
import csv

# Local Imports
from tests_get_basics import get_data_df
from util_logger import setup_logger

# Set up a global logger for this file
logger, logname = setup_logger(__name__)

# Declare our file path variables globally so they can be used in all the functions (like logger)
top100avg_csv = Path(__file__).parent.joinpath("data").joinpath("top100avg.csv")


def get_tests_server_functions(input, output, session):
    """Define functions to create UI outputs."""

    
    reactive_event = reactive.Value([])
    reactive_division = reactive.Value([])
    reactive_sex = reactive.Value([])
    reactive_data = reactive.Value()

    # Then, define our server functions
    @reactive.Effect
    @reactive.event(input.ZEROSHIFT_RESULTS)
    def _():
        reactive_data.set(input.ZEROSHIFT_RESULTS())

    @reactive.Effect
    @reactive.event(input.EVENT_DISPLAY_SELECT)
    def _():
        reactive_event.set(input.EVENT_DISPLAY_SELECT())

    @reactive.Effect
    @reactive.event(input.DIVISION_DISPLAY_SELECT)
    def _():
        reactive_division.set(input.DIVISION_DISPLAY_SELECT())

    @reactive.Effect
    @reactive.event(input.SEX_DISPLAY_SELECT)
    def _():
        reactive_sex.set(input.SEX_DISPLAY_SELECT())

    @reactive.file_reader(str(top100avg_csv))
    def get_temp_df():
        """Return pandas Dataframe."""
        logger.info(f"READING df from {top100avg_csv}")
        df = pd.read_csv(top100avg_csv, quoting=csv.QUOTE_NONE)
        logger.info(f"READING df len {len(df)}")
        return df

    @output
    @render.text
    def result_string():
        """Return a string based on selected location."""
        logger.info("tests_string starting")
        selected_event = reactive_event.get()
        selected_division = reactive_division.get()
        selected_sex = reactive_sex.get()
        line1 = f"Showing test results for the following events: {selected_event}.\n"
        line2 = f"Showing test results for the following divisions: {selected_division}.\n"
        line3 = f"Showing test results for {selected_sex}"
        message = f"{line1} {line2} {line3}"
        logger.info(f"{message}")
        return message

    @output
    @render.table
    def result_table():
        df = get_temp_df()
        # Filter the data based on the selected location
        df_result = df[(df['Sex'].isin(reactive_sex.get())) & (df['Division'].isin(reactive_division.get())) & (df['Event'].isin(reactive_event.get()))]
        logger.info(f"Rendering TEMP table with {len(df_result)} rows")
        return df_result

    @output
    @render_widget
    def result_chart():
        df = get_temp_df()
        fig = go.Figure()
        max_points = 0
        min_points = 1400
        # Filter the data based on the selected location
        if input.ZEROSHIFT_RESULTS() == "Shifted":
            shifted_df = df[df["Shift"] == "Yes"]
        else:
            shifted_df = df[df["Shift"] == "No"]
        for event in reactive_event.get():
            for division in reactive_division.get():
                for sex in reactive_sex.get():
                    df_result = shifted_df[(shifted_df['Sex'] == sex) & (shifted_df['Division'] == division) & (shifted_df['Event'] == event)]
                    max_points = max(max_points, df_result["Points"].max())
                    min_points = min(min_points, df_result["Points"].min())
                    logger.info(f"Rendering TEMP chart with {len(df_result)} points")
                    name = str(division) + " " + str(sex) + " " + str(event)
                    df_result['Name'] = name
                    fig.add_trace(go.Scatter(x=df_result["Year"], y=df_result["Points"], mode='lines+markers', name=name, hovertemplate=
                        'Year: %{x}<br>' +
                        'Points: %{y}'))
        height = max(800, ((max_points - min_points) * 5))
        fig.update_layout(title="Results for Selected Fields", xaxis_title="Year", yaxis_title="Points", legend_title="Event Description", height=height)
        return fig

    # return a list of function names for use in reactive outputs
    # Includes our 2 new selection strings and 2 new output widgets

    return [
        result_string,
        result_table,
        result_chart,
    ]