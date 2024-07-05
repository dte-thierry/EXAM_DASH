import dash 
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('nba_2013.csv')
df['age_group'] = ['rookie' if age < 24 else 'senior' for age in df['age']]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id = 'page-content')
])

# Page 0 - Accueil ---------------------------------------------------------------------

index_page = html.Div([
    html.H1('NBA Dashboard', style={'color' : 'aquamarine', 'textAlign': 'center'}),
    html.Button(dcc.Link('Comparatif de joueurs', href='/page-1')),
    html.Br(),
    html.Button(dcc.Link('Comparatif d\'équipes', href='/page-2'))
], style={'alignItems': 'center'})


# Page 1 - Comparatif de joueurs --------------------------------------------------------

layout_1 = html.Div([
    html.H1('Comparatif de joueurs', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

    html.Div(dcc.Dropdown(id = 'page-1-dropdown',
                        options= [{'label': 'rookie - joueur de moins de 24 ans', 'value': 'rookie'},
                                  {'label': 'senior - joueur de plus de 24 ans', 'value': 'senior'}],
                        value= 'rookie')),

    html.Div(id='page-1-table'),

    html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-1-table', component_property='children'),
    [Input (component_id='page-1-dropdown', component_property='value')])

def update_table(age_group):
    filtered_df = df[df["age_group"] == age_group]
    return dash_table.DataTable(data=filtered_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in filtered_df.columns])

# Page 2 - comparatif d'équipes -----------------------------------------------------------

layout_2 = html.Div([
  html.H1('Comparatif d\'équipes', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

  html.Div(dcc.Dropdown(id = 'page-2-dropdown',
                        options= [{'label': 'nombre de passes', 'value': 'ast'}],
                        value= 'ast'
  )),

  html.Div(id='page-2-graph'),

  html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-2-graph', component_property='children'),
    [Input (component_id='page-2-dropdown', component_property='value')])

def update_graph_1(indicator):
    df_grouped = df.groupby('bref_team_id')[indicator].sum().reset_index()
    df_grouped = df_grouped.nlargest(5, indicator)
    fig = px.bar(df_grouped, x='bref_team_id', y=indicator, title=f"Top 5 équipes pour {indicator}")
    return dcc.Graph(figure=fig)

# Mise à jour de l'index

@app.callback(dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/page-1':
        return layout_1
    elif pathname == '/page-2':
        return layout_2
    else:
        return index_page


# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")