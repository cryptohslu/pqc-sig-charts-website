import dash_mantine_components as dmc
from dash import html, Output, Input, callback


def create_drawer(data):
    return html.Div(
        [
            dmc.Drawer(
                title="Filter drawer",
                id="filter-drawer",
                padding="md",
                size="40%",
            ),
        ]
    )


@callback(
    Output("filter-drawer", "opened"),
    Input("filter-button", "n_clicks"),
    prevent_initial_call=True,
)
def drawer(input_value):
    return True
