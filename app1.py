import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# External Bootstrap CSS
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    }
]

# Load dataset
patients = pd.read_csv('IndividualDetails.csv')

# Aggregated statistics
total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {"label": "All", "value": "All"},
    {"label": "Hospitalized", "value": "Hospitalized"},
    {"label": "Recovered", "value": "Recovered"},
    {"label": "Deceased", "value": "Deceased"}
]

app = dash.Dash(__name__, external_stylesheets=[external_stylesheets[0]['href']])

app.layout = html.Div([
    html.H1("Corona Virus Dashboard", style={
        'textAlign': 'center', 'color': 'RoyalBlue', 'fontSize': 60., 'font-style': 'italic'}),

    # Statistics cards
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Cases", className='text-white text-center'),
                html.H4(f"{total:,}", className='text-white text-center')
            ], className='card-body bg-danger rounded')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.H3("Active Cases", className='text-white text-center'),
                html.H4(f"{active:,}", className='text-white text-center')
            ], className='card-body bg-info rounded')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.H3("Recovered", className='text-white text-center'),
                html.H4(f"{recovered:,}", className='text-white text-center')
            ], className='card-body bg-warning rounded')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.H3("Deaths", className='text-white text-center'),
                html.H4(f"{deaths:,}", className='text-white text-center')
            ], className='card-body bg-success rounded')
        ], className='col-md-3'),
    ], className='row mb-4'),

    # Filter dropdown and bar chart
    html.Div([
        html.Div([
            dcc.Dropdown(id='picker', options=options, value='All', className='mb-3'),
            dcc.Graph(id='bar')
        ], className='card-body bg-light rounded')
    ], className='row mb-4'),

    # Additional Graphs
    html.Div([
        html.Div([
            dcc.Graph(
                figure=px.pie(patients, names='current_status', title='Overall Status Distribution',
                              color_discrete_sequence=px.colors.sequential.RdBu))
        ], className='col-md-4'),

        html.Div([
            dcc.Graph(
                figure=px.sunburst(patients, path=['detected_state', 'current_status'],
                                   title='Spread by State and Status', maxdepth=2))
        ], className='col-md-4'),

        html.Div([
            dcc.Graph(
                figure=px.density_heatmap(patients, x='detected_state', y='current_status',
                                           title='State vs. Status Heatmap',
                                           color_continuous_scale='Viridis'))
        ], className='col-md-4'),
    ], className='row')
], className='container-fluid')


@app.callback(
    Output('bar', 'figure'),
    [Input('picker', 'value')]
)
def update_graph(status_type):
    if status_type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
        pbar.columns = ['state', 'count']
        return {
            'data': [go.Bar(x=pbar['state'], y=pbar['count'], marker_color='royalblue')],
            'layout': go.Layout(title='Total Cases by State', xaxis_title='State', yaxis_title='Count')
        }
    else:
        npat = patients[patients['current_status'] == status_type]
        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['state', 'count']
        return {
            'data': [go.Bar(x=pbar['state'], y=pbar['count'], marker_color='orange')],
            'layout': go.Layout(title=f'{status_type} Cases by State', xaxis_title='State', yaxis_title='Count')
        }


if __name__ == '__main__':
    app.run(debug=True)
