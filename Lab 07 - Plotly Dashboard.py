# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        # Create an id for dropdown call 'site-dropdown'
        id= 'site-dropdown',
        # Add a list of options for the dropdown menu.
        # Each option is a dictionary with label and value e.g.
        # { "label": "All Sites", "value": "ALL" }
        # { "label": "CCAFS LC-40", "value": "CCAFS LC-40" }
        options=[
            {"label":"All Sites", "value":"ALL"},
            {"label":"CCAFS LC-40", "value":"CCAFS LC-40"},
            {"label":"VAFB SLC-4E", "value":"VAFB SLC-4E"},
            {"label":"KSC LC-39A", "value":"KSC LC-39A"},
            {"label":"CCAFS SLC-40", "value":"CCAFS SLC-40"},
        ],
        # Set the default value of the dropdown to 'ALL'
        value="ALL",
        # Create a placeholder for the drop down
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        # Create an id for slider call 'payload-slider'
        id="payload-slider",
        # Set minimum slider value to 0
        min=0,
        # Set maximum slider value to 10000
        max=10000,
        # Set slider step to 1000
        step=1000,
        # Set default value of slider to min and max of payload
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    dcc.Graph(id='success-payload-scatter-chart'),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Connect the pie chart to dropdown menu
@app.callback(
    # Add an Ouput to render graph
    Output(component_id="success-pie-chart", component_property="figure"),
    # Add an Input to read value from dropdown
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    # The dropdown selected value is pass as argument 'entered_site'

    # If the user selected All Sites ...
    if entered_site == "ALL":
        # ... Return the number of luanches from each site as a pie chart
        dff = spacex_df[spacex_df["class"] == 1]
        return px.pie(
            names=dff["Launch Site"].value_counts().index,
            values=dff["Launch Site"].value_counts().values)

    else:
        # If the user selected a particular launch site
        # show the number of failed and success launches in a pie chart
        dff = spacex_df[spacex_df["Launch Site"] == entered_site]
        return px.pie(
            names=spacex_df["class"].value_counts().index,
            values=dff["class"].value_counts().values)



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value")
    ],
)
def get_scatter_chart(entered_site, payload_range):

    # The chart is affected by two inputs (dropdown and slider)
    # The dropdown selection is passed as argument to 'entered_site'
    # The selected range is passed as argument 'payload_range'

    # Filter dataframe to get payloads between payload range
    min_value, max_value = payload_range
    dff = spacex_df[spacex_df["Payload Mass (kg)"].between(min_value, max_value)]

    # If the user selected ALL sites
    if entered_site == "ALL":
        # Plot the scatter chart with payload at x axis and class at y axis
        # Set color of the points using "Booster Version Category"
        return px.scatter(dff, x = "Payload Mass (kg)", y = "class", color="Booster Version Category")

    else:
        # If the user selected a particular site
        # Filter the dataframe with only the launch site
        dff = dff[dff["Launch Site"] == entered_site]
        # Plot the scatter chart with payload at x axis and class at y axis
        # Set color of the points using "Booster Version Category"
        return px.scatter(dff, x = "Payload Mass (kg)", y = "class", color="Booster Version Category")



# Run the app
if __name__ == '__main__':
    app.run_server()
