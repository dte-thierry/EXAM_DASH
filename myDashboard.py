import dash
import dash_bootstrap_components as dbc 
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('nba_2013.csv')
df['age_group'] = ['rookie' if age < 24 else 'senior' for age in df['age']]

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

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
                                  {'label': 'senior - joueur de plus de 24 ans', 'value': 'senior'},
                                  {'label': 'Top 5 des meilleurs joueurs', 'value': 'top_players'}],  # Ajout de l'option 'top_players'
                        value= 'rookie')),

    
    html.Div(id='page-1-table'),  

    html.Div(id='page-1-top-players'),  # Nouveau Div pour les cartes de joueurs  

    html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-1-table', component_property='children'),
    [Input (component_id='page-1-dropdown', component_property='value')])

def update_page_content(value):
    if value in ['rookie', 'senior']:
        filtered_df = df[df["age_group"] == value]
        return dash_table.DataTable(data=filtered_df.to_dict('records'), columns=[{'name': i, 'id': i} for i in filtered_df.columns])
    elif value == 'top_players':
        top_players = df.nlargest(5, 'pts')  # Sélectionnez les 5 meilleurs joueurs
        cards = []
        for _, player in top_players.iterrows():
            card_content = [
                html.H5(f"{player['player']}", className="card-title"),
                html.P(f"Points: {player['pts']}", className="card-text"),
            ]
            card = html.Div(
                dbc.Card(card_content, color="primary", inverse=True),
                className="col-md-8",
                style={"maxWidth": "260px"},
            )
            cards.append(card)
        return cards


# Page 2 - comparatif d'équipes -----------------------------------------------------------

layout_2 = html.Div([
  html.H1('Comparatif d\'équipes', style={'textAlign': 'center', 'color': 'mediumturquoise'}),

  html.Div(dcc.Dropdown(id = 'page-2-dropdown',
                        options= [{'label': 'nombre de passes décisives - ast -', 'value': 'ast'},
                                  {'label': 'nombre de rebonds offensifs - orb -', 'value': 'orb'}],  # Ajout de l'option orb
                        value= 'ast'
  )),

  html.Div(dcc.Slider(id='page-2-slider',
                      min=0,
                      max=4,
                      step=None,
                      marks={0: 'Point Guard', 1: 'Power Forward', 2: 'Center', 3: 'Small Forward', 4: 'Shooting Guard'},
                      value=0)),  # change 'PG' to 0
  
  html.Br(),
  
  html.Div(id='page-2-graph'),

  html.Button(dcc.Link('Retour à la page d\'accueil', href='/'))

], style = {'background' : 'beige'})

@app.callback(Output (component_id='page-2-graph', component_property='children'),
              [Input (component_id='page-2-dropdown', component_property='value'),
               Input (component_id='page-2-slider', component_property='value')])

def update_graph(indicator, pos):
    pos_map = {0: 'PG', 1: 'PF', 2: 'C', 3: 'SF', 4: 'SG'}
    df_filtered = df[df['pos'] == pos_map[pos]]
    df_grouped = df_filtered.groupby('bref_team_id')[indicator].sum().reset_index()
    df_grouped = df_grouped.nlargest(5, indicator)
    fig = px.bar(df_grouped, x='bref_team_id', y=indicator, title=f"Top 5 des équipes comprenant les : <br>Point Guard (PG), Power Forward (PF), Center (C), Small Forward (SF), Shooting Guard (SG) - ind: {pos_map[pos]} -")
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