# Importer les bibliothèques nécessaires
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Créer une base de données fictive
data = {
    'Région': ['Auvergne-Rhône-Alpes', 'Bretagne', 'Corse', 'Grand Est', 'Hauts-de-France', 'Île-de-France', 'Normandie', 'Nouvelle-Aquitaine', 'Occitanie', 'Pays de la Loire', 'Provence-Alpes-Côte d\'Azur'],
    'Taux': [5, 10, 3, 7, 8, 12, 6, 9, 11, 5, 10]
}

df = pd.DataFrame(data)
df = df.sort_values(by='Taux', ascending=False)

# Créer l'application Dash
app = dash.Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div([
    html.Div("Coucou Kiki Loulou", style={
        'backgroundColor': 'black',
        'color': 'white',
        'fontStyle': 'italic',
        'padding': '30px 10px',
        'fontSize': '36px',
        'textAlign': 'center'
    }),
    dcc.Graph(id='bar-graph', 
              config={'staticPlot': False, 'displayModeBar': True},
              style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='scatter-plot', style={'width': '50%', 'display': 'inline-block'}),
    html.Div("Comment bien faire une passe", style={
        'padding': '10px',
        'fontSize': '20px',
        'textAlign': 'center'
    }),
    # Ajout de l'image
    html.Img(src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-GDBi86JV1DCfwNs6-1vAD9i8thTqXbwe0A&usqp=CAU", 
             style={
                 'display': 'block',
                 'margin-left': 'auto',
                 'margin-right': 'auto',
                 'width': '500px'
            }
    )
    #html.Div(id='output')
])

@app.callback(
    [Output('bar-graph', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('bar-graph', 'clickData')]
)
def update_graph(clicked_data):
    bar_figure = px.bar(df, x='Région', y='Taux', title="Taux par Région")
    bar_figure.update_xaxes(title_text='')

    if clicked_data:
        selected_region = clicked_data['points'][0]['x']
        sizes = [30 if region == selected_region else 10 for region in df['Région']]
        colors = ['red' if region == selected_region else 'blue' for region in df['Région']]
    else:
        sizes = [10] * df.shape[0]
        colors = ['blue'] * df.shape[0]

    scatter_figure = px.scatter(df, x='Région', y='Taux', title="Nuage de Points des Taux par Région")
    scatter_figure.update_traces(marker=dict(size=sizes, color=colors))
    scatter_figure.update_xaxes(title_text='')

    return bar_figure, scatter_figure

if __name__ == '__main__':
    app.run_server(debug=True,port  = 9697)