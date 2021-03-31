import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import graphs

app = dash.Dash(__name__,
                title="MoMA on Tour", suppress_callback_exceptions=True)

app.layout = dcc.Loading(
    html.Div(
        children=[
            #1st row
            html.Div(
                children=[
                #1st column
                html.Div(
                    children=[
                    html.Div(
                        children=[
                            html.Img(
                                src=app.get_asset_url("moma-logo.png"),
                                style={'width': '180%', 'margin-top': '0px'}
                            ),
                        ],
                    style={'width': '25%'}
                    ),
                        html.Div(
                            children=[
                                html.H5('The Museum of Modern Art (MoMA) acquired its first artworks in 1929.'
                                        ' Today, the Museum’s evolving collection contains almost 200,000 works'
                                        ' from around the world spanning the last 150 years. In this dashboard, '
                                        'you can go on tour with the MoMA museum by getting insights into which '
                                        'artworks it acquired over the years and by which artists. Next, you can '
                                        'see MoMA per country by checking which country the art pieces come from. '
                                        'The art collections include an ever-expanding range of visual expression, '
                                        'including painting, sculpture, photography, architecture, design, and '
                                        'film art. Travel through time and space with MoMA and enjoy the tour...'),
                                ],
                                className='card',
                                style={"height": "25%"},
                        ),
                        html.Div(
                            dcc.Graph(
                                figure=graphs.line_chart_nationalities(),
                                className='card',
                                style={"height": "60%"},
                            ),
                        ),
                    ],
                    className='body',
                    style={'width': '50%'}
                ),
                #2nd column
                html.Div(
                    children=[
                        dcc.Loading([
                                dcc.Graph(figure=graphs.map_with_animation(),
                                          id='main-choropleth')],
                                type='default', color='black', id="map-loading")
                    ],
                    className='card',
                    style={'width': '50%', 'margin-bottom': '7px'}
                ),
            ],
            className='container'
        ),

        #2nd row
        html.Div(
            children=[
                    dcc.Graph(
                        figure=graphs.genders_chart(),
                        className='card',
                        style={
                            "width": "40%"
                        }
                    ),
                    dcc.Graph(
                        figure=graphs.bar_with_animation(),
                        className='card',
                        style={
                            "width": "55%"
                        }
                    ),
            ],
            className='container'
        ),

        #3rd row
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H2("Choose countries"),
                                        dcc.Dropdown(
                                            options=[{'label': v, 'value': v}
                                                     for v in graphs.unique_countries()],
                                            multi=True,
                                            id='countries-dropdown'),
                                    ],
                                    className='first card',
                                    style={'width': '40%', 'float': 'right'}
                                ),
                html.Div(children=[
                    html.H2('Artists'),
                    html.H3('123', id='unique-artists')
                ],
                    className='card small'
                ),
                html.Div(
                    children=[
                        html.H2('Artworks'),
                        html.H3('123', id='unique-artworks')
                    ],
                    className='card small'
                ),
                html.Div(
                    children=[
                        html.H2('Gender'),
                        html.H3('Male:'),
                        html.H3('123%', id='male-count'),
                        html.H3(' Female:'),
                        html.H3('123%', id='female-count')
                    ],
                    className=' card small'
                ),
            ],
            className='container'
        ),

        #4th row
        html.Div(
            children=[
                dcc.Graph(
                    figure=graphs.sunburst(),
                    className='card',
                    style={'width': '50%'},
                    id='sunburst'
                ),
                dcc.Graph(
                    figure=graphs.donut_chart(),
                    className='card',
                    style={'width': '50%'},
                    id='donut'
                )

            ],
            className='container'
        ),



        html.Footer([
            html.Label(["Anastasiia Tagiltseva, m20200041 | Beatriz Pereira, m20200674 | Nadine Aldesouky, m20200568 | Svitlana Vasylyeva, m20200617| "
                    "Source: ", html.A("MoMA",
                                          href="https://github.com/MuseumofModernArt/collection", target="_blank")])

    ],
        className="footer"
    ),
    ]),
    type = 'cube',  color='white')


@app.callback(
    Output('unique-artists', 'children'),
    Output('unique-artworks', 'children'),
    Output('male-count', 'children'),
    Output('female-count', 'children'),
    Output('sunburst', 'figure'),
    Output('donut', 'figure'),
    Input('countries-dropdown', 'value')
)
def update_stats(value):
    stats = graphs.statistics(value)
    return stats[0], stats[1], stats[2], stats[3], graphs.sunburst(value), graphs.donut_chart(value)


if __name__ == '__main__':
    app.run_server(debug=True)
