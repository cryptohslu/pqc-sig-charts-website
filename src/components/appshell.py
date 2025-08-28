import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, page_container

from components.header import create_header
from components.navbar import create_navbar


def create_appshell(data, url_base_pathname):
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="dark",
        children=[
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            dmc.NotificationProvider(),
            dmc.AppShell(
                [
                    create_header(data, url_base_pathname),
                    create_navbar(data),
                    dmc.AppShellMain(children=page_container),
                ],
                header={"height": 70},
                padding="xl",
                navbar={
                    "width": 425,
                    "breakpoint": "sm",
                    "collapsed": {"mobile": True, "desktop": False},
                },
                id="appshell",
            ),
        ],
    )


@callback(
    Output("appshell", "navbar"),
    [
        Input("filter-button", "n_clicks"),
        Input("url", "pathname"),
    ],
    State("appshell", "navbar"),
    prevent_initial_call=True,
)
def toggle_navbar(n_clicks, url, navbar):
    if url == "/sig-charts/compare/":
        navbar["collapsed"] = {
            "mobile": True,
            "desktop": True,
        }
    elif n_clicks % 2 == 0:
        navbar["collapsed"] = {
            "mobile": True,
            "desktop": False,
        }
    else:
        navbar["collapsed"] = {
            "mobile": True,
            "desktop": True,
        }
    return navbar
