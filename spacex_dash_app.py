# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
opt = list(set(spacex_df['Launch Site']))
opt = ['All Sites'] + opt
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                dcc.Dropdown(id='id',
                options=opt,
                value='All Sites',
                placeholder="place holder here",
                searchable=True
                ),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step = 1000, value = [2500,7500],marks={0: '0',2500: '2500', '5000' : 5000, '7500' : 7500, '10000':10000})),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='id', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    print(entered_site)
    if entered_site == 'All Sites':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title=entered_site)
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        d = filtered_df.groupby('class').count()
        print(d)
        d = d.reset_index()
        fig = px.pie(d, values='Unnamed: 0', 
        names='class', 
        title=entered_site)
        return fig

        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='id', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(site, mass):
    print(mass)
    d = spacex_df[(spacex_df['Payload Mass (kg)'] >= mass[0]) & (spacex_df['Payload Mass (kg)'] <= mass[1])]
    print(d)
    if site == 'All Sites':
        fig = px.scatter(x = d['Payload Mass (kg)'], y = d['class'], color = d['Booster Version Category'])
        return fig
    else:
        d = d[d['Launch Site'] == site]
        fig = px.scatter(x = d['Payload Mass (kg)'], y = d['class'], color = d['Booster Version Category'])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
