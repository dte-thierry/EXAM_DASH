import dash 
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv('nba_2013.csv')
df['age_group'] = ['rookie' if age < 24 else 'senior' for age in df['age']]

# Initialiser l'application Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

# Définir la mise en page de l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1("Page d'accueil", style={'color' : 'aquamarine', 'textAlign': 'center'}),
    html.Button('Comparatif de joueurs', id='compare-button'),
])

compare_page = html.Div([
    html.H1("Comparatif de joueurs"),
    dcc.Dropdown(
        id='rookie-dropdown',
        options=[{'label': i, 'value': i} for i in df[df['age_group'] == 'rookie']['player'].unique()],
        placeholder="Sélectionnez un rookie"
    ),
    dcc.Dropdown(
        id='senior-dropdown',
        options=[{'label': i, 'value': i} for i in df[df['age_group'] == 'senior']['player'].unique()],
        placeholder="Sélectionnez un senior"
    ),
    html.Div(id='display-selected-values'),
    html.Button('Retour', id='back-button'),
])

# Mettre à jour la page en fonction de l'URL
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/compare':
        return compare_page
    else:
        return index_page
    
# Naviguer vers la page de comparaison lorsque le bouton est cliqué
@app.callback(Output('url', 'pathname'),
              [Input('compare-button', 'n_clicks'), Input('back-button', 'n_clicks')])
def navigate(n_clicks_compare, n_clicks_back):
    ctx = dash.callback_context

    # Vérifier quel bouton a été cliqué
    if not ctx.triggered:
        return '/'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'compare-button' and n_clicks_compare:
        return '/compare'
    elif button_id == 'back-button' and n_clicks_back:
        return '/'

# Afficher les statistiques des joueurs sélectionnés
@app.callback(Output('display-selected-values', 'children'),
              Input('rookie-dropdown', 'value'),
              Input('senior-dropdown', 'value'))
def display_selected_values(rookie, senior):
    if rookie and senior:
        rookie_stats = df[df['player'] == rookie].iloc[0]
        senior_stats = df[df['player'] == senior].iloc[0]
        return html.Div([
            html.H2("Statistiques du rookie"),
            html.P(rookie_stats.to_string()),
            html.H2("Statistiques du senior"),
            html.P(senior_stats.to_string()),
        ])

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0")