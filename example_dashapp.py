# app.py

import pandas as pd
from dash import Dash, dcc, html
from plotnine import ggplot, aes, labs, geom_point
from plotnine.data import mpg
from plotly.tools import mpl_to_plotly

# from dash.dependencies import Input, Output
# Bon  à savoir :  l'application DASH s'actualise en direct !!!! en checkant le code

# Télécharger les données ici !! https://www.kaggle.com/datasets/neuromusic/avocado-prices
# installer ngrok et mettre à dis^po sur le we via ngrok http port sur serveur local de l'app
data = (
    pd.read_csv("avocado.csv")
    .query("type == 'conventional' and region == 'Albany'")
    .assign(Date=lambda data: pd.to_datetime(data["Date"], format="%Y-%m-%d"))
    .sort_values(by="Date")
)


# Create a ggplot graph using plotnine
p = ggplot(aes(x='displ', y='cty'), mpg)
p += geom_point()

# Save the ggplot output as an image file
image_name = "ggplot_output.png"
ggplot_image_path = "assets/"+image_name
p.save(ggplot_image_path, dpi=150)



external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]




app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "C'est bon les avocats !"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocats !!!", className="header-title"
                ),
                html.P(
                    children=(
                        "Mange des avocats pour être bon au volley !",html.Br(),
                        "Voici les ventes aux US entre 2015 et 2018"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["AveragePrice"],
                                    "type": "lines",
                                    "hovertemplate": (
                                        "$%{y:.2f}<extra></extra>"
                                    ),
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Average Price of Avocados",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17b897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Total Volume"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Avocados Sold",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Markdown(
                        '''
                        ## LaTeX in a Markdown component:

                        This example uses the block delimiter:
                        $$
                        \\frac{1}{(\\sqrt{\\phi \\sqrt{5}}-\\phi) e^{\\frac25 \\pi}} =
                        1+\\frac{e^{-2\\pi}} {1+\\frac{e^{-4\\pi}} {1+\\frac{e^{-6\\pi}}
                        {1+\\frac{e^{-8\\pi}} {1+\\ldots} } } }
                        $$

                        This example uses the inline delimiter:
                        $E^2=m^2c^4+p^2c^2$
                        ''',
                        mathjax=True
                    ),
                    className="card"
                ),
                html.Div(
                    children=html.Img(
                        src=app.get_asset_url(image_name),
                    ),
                    className ="card"
                ),
            ],
            className="wrapper",
        ),
    ]
)
        
if __name__ == "__main__":
    app.run_server(debug=True, port=8089)
