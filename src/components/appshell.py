import dash_mantine_components as dmc
from dash import (
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    page_container,
)

from components.dataset import DATASETS
from components.header import create_header
from components.navbar import create_navbar


def create_appshell(data, url_base_pathname):
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="dark",
        children=[
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            dmc.NotificationContainer(),
            dmc.AppShell(
                [
                    create_header(data, url_base_pathname),
                    create_navbar(data),
                    dmc.AppShellMain(
                        children=[
                            html.Div(id="tour-placeholder", style={"display": "none"}),
                            html.Button(id="tour-preselect-btn", n_clicks=0, style={"display": "none"}),
                            html.Button(id="tour-clear-btn", n_clicks=0, style={"display": "none"}),
                            html.Button(id="tour-compare-dataset-btn", n_clicks=0, style={"display": "none"}),
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
                                gap="xl",
                                style={"marginTop": "-50px"},
                            ),
                            dmc.Box(
                                id="compare-dataset-controls",
                                style={"display": "none"},
                                children=dmc.Group(
                                    justify="center",
                                    p="md",
                                    children=dmc.Select(
                                        id="compare-dataset-selector",
                                        label="Compare against",
                                        placeholder="Select a second dataset to compare",
                                        data=[{"value": k, "label": v} for k, v in DATASETS.items()],
                                        allowDeselect=True,
                                        checkIconPosition="right",
                                        clearable=True,
                                        w=400,
                                    ),
                                ),
                            ),
                        ]
                    ),
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


clientside_callback(
    """
    function(pathname, clickedAlgs) {
        const isCompare = pathname === '/sig-charts/compare/' || pathname === '/sig-charts/compare';
        const hasAlgs = clickedAlgs && Object.values(clickedAlgs).some(Boolean);
        return (isCompare && hasAlgs) ? {"display": "block"} : {"display": "none"};
    }
    """,
    Output("compare-dataset-controls", "style"),
    Input("url", "pathname"),
    Input("clicked-algs", "data"),
)


@callback(
    Output("compare-dataset-selector", "data"),
    Output("compare-dataset-selector", "value"),
    Input("dataset-selector", "value"),
)
def sync_compare_selector(base_dataset):
    filtered = [{"value": k, "label": v} for k, v in DATASETS.items() if k != base_dataset]
    return filtered, None


@callback(
    Output("compare-dataset-selector", "value", allow_duplicate=True),
    Input("tour-compare-dataset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def set_tour_compare_dataset(_):
    return "dataset_v6_x86_64_c8a.large.zst"


@callback(
    Output("compare-dataset-selector", "value", allow_duplicate=True),
    Input("tour-clear-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_tour_compare_dataset(_):
    return None


clientside_callback(
    """
    function(pathname) {
        if (!window.pqcTour) return '';
        if (pathname === '/sig-charts/' || pathname === '/sig-charts') {
            window.pqcTour.startOverview(false);
        } else if (pathname === '/sig-charts/compare/' || pathname === '/sig-charts/compare') {
            window.pqcTour.startCompare();
        }
        return '';
    }
    """,
    Output("tour-placeholder", "children"),
    Input("url", "pathname"),
)
