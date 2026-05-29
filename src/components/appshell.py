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
                    dmc.AppShellMain(children=[
                        page_container,
                        dmc.SimpleGrid(
                            id="content-overview",
                            type="container",
                            cols={
                                "base": 1,
                                "500px": 2,
                                "750px": 3,
                                "1000px": 4,
                                "1250px": 5,
                                "1500px": 6,
                                "1750px": 7,
                                "2000px": 8,
                                "2250px": 9,
                                "2500px": 10,
                            },
                            spacing=0,
                            verticalSpacing="xs",
                        ),
                        dmc.Stack(
                            id="content-compare",
                            align="center",
                            justify="flex-start",
                            gap=0,
                        ),
                    ]),
                ],
                header={"height": 70},
                padding="xl",
                navbar={
                    "width": 370,
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
)
def toggle_navbar(n_clicks, url, navbar):
    if url == "/sig-charts/compare/":
        navbar["collapsed"] = {
            "mobile": True,
            "desktop": True,
        }
    elif n_clicks is not None and n_clicks > 0:
        if n_clicks % 2 == 0:
            navbar["collapsed"] = {
                "mobile": False,
                "desktop": False,
            }
        else:
            navbar["collapsed"] = {
                "mobile": True,
                "desktop": True,
            }
    else:
        # Navigating back from compare with no filter button interaction:
        # restore the default state (visible on desktop, hidden on mobile).
        navbar["collapsed"] = {
            "mobile": True,
            "desktop": False,
        }
    return navbar
