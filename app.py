import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output

#External Bootstrap CSS
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('IndividualDetails.csv')

total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered  = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {"label": "All", "value": "All"},
    {"label": "Hospitalized", "value": "Hospitalized"},
    {"label": "Recovered", "value": "Recovered"},
    {"label": "Deceased", "value": "Deceased"}
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H1("Corona Virus Dashboard", style={'textAlign': 'center', 'color': 'RoyalBlue', 'fontSize': 60., 'font_style': 'italic'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", style={'textAlign': 'center', 'color': 'white', 'fontSize': 30.}),
                    html.H4(total, style={'textAlign': 'center', 'color': 'white', 'fontSize': 40.,'font_style': 'bold'})
                ],className='card-body')
            ],className='card bg-danger'),
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", style={'textAlign': 'center', 'color': 'white', 'fontSize': 30.}),
                    html.H4(active, style={'textAlign': 'center', 'color': 'white', 'fontSize': 40.})
                ],className='card-body')
            ],className='card bg-info'),
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", style={'textAlign': 'center', 'color': 'white', 'fontSize': 30.}),
                    html.H4(recovered, style={'textAlign': 'center', 'color': 'white', 'fontSize': 40.})
                ],className='card-body')
            ],className='card bg-warning'),
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", style={'textAlign': 'center', 'color': 'white', 'fontSize': 30.}),
                    html.H4(deaths, style={'textAlign': 'center', 'color': 'white', 'fontSize': 40.})
                ],className='card-body')
            ],className='card bg-success'),
        ], className='col-md-3')
    ], className='row'),
    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id = 'picker', options = options, value = 'All'),
                    dcc.Graph(id = 'bar'),
                ], className='card-body'),
            ], className='card'),
        ], className='col-md-12'),
    ], className='row'),

], className='container')


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
        npat = patients[patients['current_status'] == status_type]  # Ensure this column exists!
        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['state', 'count']
        return {
            'data': [go.Bar(x=pbar['state'], y=pbar['count'], marker_color='orange')],
            'layout': go.Layout(title=f'{status_type} Cases by State', xaxis_title='State', yaxis_title='Count')
        }


if __name__ == '__main__':
    app.run(debug=True)
