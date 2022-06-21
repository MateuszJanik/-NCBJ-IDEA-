"""
A file to manage and run dash frontend.

"""
import dash_cytoscape as cyto
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from manage_data import PrepareData, FILE_NAME

APP = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def create_plot_card(card_id, title, plot_id, fig):
    """
    The function to create card from bootstrap.

            Parameters:
                    card_id (str): string id
                    title (str): string title
                    plot_id (str): string plot id
                    fig(obj): graph object

            Returns:
                    dbc.Card (dbc.Card): returns dbc.Card from bootstrap
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                dcc.Graph(id=plot_id, figure=fig, style={'display': 'inline-block'})
            ]
        )
    )


def create_graph_card(card_id, title, prepared_data):
    """
    The function to create card from bootstrap.

            Parameters:
                    card_id (str): string id
                    title (str): string title
                    prepared_data (pd.Dataframe): the data needed to generate the chart

            Returns:
                    dbc.Card (dbc.Card): returns dbc.Card from bootstrap
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, id=f"{card_id}-title"),
                cyto.Cytoscape(
                    id='cytoscape-two-nodes',
                    layout={'name': 'breadthfirst'},
                    style={'width': '600px', 'height': '977px', 'display': 'inline-block'},
                    stylesheet=[{
                        "selector": "edge",
                        "style": {"label": "data(label)"}
                    },
                        {
                            "selector": "node",
                            "style": {"label": "data(label)"}
                        }
                    ],
                    elements=prepared_data,
                )
            ]
        )
    )


@APP.callback(
    Output('our4-plot', 'figure'),
    Input('my_numeric_input_cluster', 'value'),
    Input('my_numeric_input_hour', 'value'),
)
def update_output(my_numeric_input_cluster, my_numeric_input_hour):
    """
    The function to create a subdivision into clusters.

            Parameters:
                    my_numeric_input_cluster (int): number of clusters
                    my_numeric_input_hour (int): number of hour

            Returns:
                    cluster_plot (obj): returns the cluster plot
    """

    branches_cluster_data = PrepareData.simple_cluster(PREPARED_FILE_DATA, my_numeric_input_hour,
                                                       my_numeric_input_cluster)
    cluster_plot = px.scatter(branches_cluster_data, x="branch_id", y="flow_[MW]", color='cluster')
    return cluster_plot


PREPARED_FILE_DATA = PrepareData.extract_data(FILE_NAME)
NODES_AND_BRANCHES_GRAPH = PrepareData.generate_nodes_and_branches(PREPARED_FILE_DATA)
PREPARED_NODES_BAR_PLOT_DATA = PrepareData.nodes_bar_plot_data(PREPARED_FILE_DATA)
PREPARED_BRANCHES_BAR_PLOT_DATA = PrepareData.branches_bar_plot_data(PREPARED_FILE_DATA)
PREPARED_BRANCHES_CLUSTER_DATA = PrepareData.simple_cluster(PREPARED_FILE_DATA, 1, 1)

NODES_BAR_PLOT_DEMANDS = px.bar(PREPARED_NODES_BAR_PLOT_DATA, x="node_id", y="demand_[MW]",
                                animation_frame="hour", animation_group="demand_[MW]", range_y=[0, 32],
                                hover_data=['cost_[zl]', "generation_[MW]"], barmode='group')

NODES_BAR_PLOT_GENERATION = px.bar(PREPARED_NODES_BAR_PLOT_DATA, x="node_id", y="generation_[MW]",
                                   animation_frame="hour", animation_group="generation_[MW]", range_y=[0, 32],
                                   hover_data=['cost_[zl]', "demand_[MW]"])

BRANCHES_BAR_PLOT = px.bar(PREPARED_BRANCHES_BAR_PLOT_DATA, x="branch_id", y="flow_[MW]",
                           animation_frame="hour", animation_group="flow_[MW]", range_y=[-20, 20], barmode='group')

BRANCHES_CLUSTER_PLOT = px.scatter(PREPARED_BRANCHES_CLUSTER_DATA, x="branch_id", y="flow_[MW]", color='cluster')

APP.layout = html.Div([
    dbc.Row([
        dbc.Col([create_plot_card('id1', 'nodes_demands_bar_plot', 'our1-plot', NODES_BAR_PLOT_DEMANDS),
                 create_plot_card('id5', 'nodes_generation_bar_plot', 'our5-plot', NODES_BAR_PLOT_GENERATION)]),
        dbc.Col([create_graph_card('id2', 'graph', NODES_AND_BRANCHES_GRAPH)])
    ]),
    dbc.Row([
        dbc.Col([create_plot_card('id3', 'BRANCHES_BAR_PLOT', 'our3-plot', BRANCHES_BAR_PLOT)]),
        dbc.Col(dbc.Card(
            dbc.CardBody(
                [
                    html.H4("clusters", id="id4"),
                    html.H6("number_of_clusters:", id="id8"),
                    html.Div([
                        daq.NumericInput(
                            min=1,
                            max=len(PREPARED_BRANCHES_CLUSTER_DATA),
                            id='my_numeric_input_cluster',
                            value=1,
                        ),
                    ]),
                    html.H6("hour:", id="id9"),
                    html.Div([
                        daq.NumericInput(
                            min=0,
                            max=24,
                            id='my_numeric_input_hour',
                            value=1,
                        ),
                    ]),
                    dcc.Graph(id="our4-plot", figure=BRANCHES_CLUSTER_PLOT, style={'display': 'inline-block'})
                ]
            )
        )),
    ]),

])

if __name__ == '__main__':
    APP.run_server()
