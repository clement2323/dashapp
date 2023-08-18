# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample dataset
data = {
    'Région': ['Auvergne-Rhône-Alpes', 'Bretagne', 'Corse', 'Grand Est', 
               'Hauts-de-France', 'Île-de-France', 'Normandie', 'Nouvelle-Aquitaine', 
               'Occitanie', 'Pays de la Loire', 'Provence-Alpes-Côte d\'Azur'],
    'Taux': [5, 10, 3, 7, 8, 12, 6, 9, 11, 5, 10]
}
df = pd.DataFrame(data)
df.sort_values(by='Taux', inplace=True, ascending=False)

# Create the Dash app
app = dash.Dash(__name__)

# Stylish layout
app.layout = html.Div([
    html.Div("Analysis of Taux by Région", style={
        'backgroundColor': '#34495E',
        'color': '#ECF0F1',
        'padding': '30px',
        'fontSize': '36px',
        'textAlign': 'center',
        'borderRadius': '8px',
        'margin': '20px'
    }),
    dcc.Graph(id='bar-graph', 
              config={'staticPlot': False, 'displayModeBar': True},
              style={'width': '50%', 'display': 'inline-block'}),
    dcc.Graph(id='scatter-plot', 
              style={'width': '50%', 'display': 'inline-block'}),
    html.Div("Detailed Overview", style={
        'padding': '20px',
        'fontSize': '24px',
        'textAlign': 'center',
        'marginTop': '20px',
        'backgroundColor': '#7F8C8D',
        'color': '#FDFEFE',
        'borderRadius': '8px',
        'margin': '20px'
    }),
    html.Img(src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-GDBi86JV1DCfwNs6-1vAD9i8thTqXbwe0A&usqp=CAU", 
             style={
                 'display': 'block',
                 'margin': '20px auto',
                 'width': '400px',
                 'borderRadius': '8px',
                 'boxShadow': '5px 5px 15px #888888'
            }
    )
], style={'backgroundColor': '#EAEDED', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0px 0px 15px #888888'})

@app.callback(
    [Output('bar-graph', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('bar-graph', 'clickData')]
)
def update_graph(clicked_data):
    bar_figure = px.bar(df, x='Région', y='Taux', title="Taux Distribution by Région", 
                        color_discrete_sequence=["#3498DB"])
    bar_figure.update_xaxes(title_text='')
    bar_figure.update_layout(paper_bgcolor="#EAEDED", plot_bgcolor="#EAEDED")

    if clicked_data:
        selected_region = clicked_data['points'][0]['x']
        sizes = [30 if region == selected_region else 10 for region in df['Région']]
        colors = ['red' if region == selected_region else '#3498DB' for region in df['Région']]
    else:
        sizes = [10] * df.shape[0]
        colors = ['#3498DB'] * df.shape[0]

    scatter_figure = px.scatter(df, x='Région', y='Taux', title="Scatter Plot of Taux by Région")
    scatter_figure.update_traces(marker=dict(size=sizes, color=colors))
    scatter_figure.update_xaxes(title_text='')
    scatter_figure.update_layout(paper_bgcolor="#EAEDED", plot_bgcolor="#EAEDED")

    return bar_figure, scatter_figure

if __name__ == '__main__':
    app.run_server(debug=True, port=9697)
