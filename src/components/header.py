import dash_mantine_components as dmc
from dash import Input, Output, callback, clientside_callback, dcc, html, no_update
from dash_iconify import DashIconify

from components.dataset import ALL_DATA, DEFAULT_DATASET

_DEFAULT_N_ALGS = len(ALL_DATA[DEFAULT_DATASET])

theme_toggle = dmc.Switch(
    offLabel=DashIconify(icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id="color-scheme-toggle",
    persistence=True,
    color="grey",
)


def create_header(data, url_base_pathname):
    return dmc.AppShellHeader(
        px=25,
        children=[
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="n-selected-algs", storage_type="session"),
            dcc.Store(id="selected-algs", storage_type="session"),
            dcc.Store(id="n-clicked-algs", storage_type="session"),
            dcc.Store(id="clicked-algs", storage_type="session"),
            dmc.Stack(
                justify="center",
                h=70,
                children=dmc.Grid(
                    justify="space-between",
                    children=[
                        dmc.GridCol(
                            dmc.Group(
                                [
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="clarity:filter-grid-circle-solid",
                                            width=20,
                                        ),
                                        id="filter-button",
                                        size="lg",
                                        variant="light",
                                        radius="xl",
                                        n_clicks=0,
                                    ),
                                    dmc.Anchor(
                                        [f"PQC Signatures ({_DEFAULT_N_ALGS} / {_DEFAULT_N_ALGS})"],
                                        id="website-title",
                                        href=url_base_pathname,
                                        underline=False,
                                    ),
                                ]
                            ),
                            span="content",
                        ),
                        dmc.GridCol(
                            span="auto",
                            children=dmc.Group(
                                justify="flex-end",
                                h=31,
                                gap="xl",
                                children=[
                                    dmc.Anchor(
                                        dmc.Button(
                                            "Overview",
                                            variant="subtle",
                                            id="overview-button",
                                        ),
                                        href="/sig-charts/",
                                        visibleFrom="sm",
                                    ),
                                    dmc.Anchor(
                                        dmc.Button(
                                            "Compare",
                                            variant="subtle",
                                            id="compare-button",
                                        ),
                                        href="/sig-charts/compare/",
                                        visibleFrom="sm",
                                    ),
                                    dmc.Anchor(
                                        dmc.Button(
                                            "Applied Cyber Security Research Lab",
                                            variant="subtle",
                                        ),
                                        href="https://www.hslu.ch/en/acs/",
                                        target="_blank",
                                        visibleFrom="md",
                                    ),
                                    dmc.Tooltip(
                                        label="Replay tour",
                                        position="bottom",
                                        children=dmc.ActionIcon(
                                            DashIconify(icon="tabler:help", width=18),
                                            id="tour-restart-button",
                                            size="lg",
                                            variant="subtle",
                                            radius="xl",
                                            n_clicks=0,
                                        ),
                                    ),
                                    theme_toggle,
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-toggle", "id"),
    Input("color-scheme-toggle", "checked"),
)

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0 && window.pqcTour) {
            window.pqcTour.restart();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("tour-restart-button", "id"),
    Input("tour-restart-button", "n_clicks"),
)


@callback(
    [
        Output("clicked-algs", "data", allow_duplicate=True),
        Output("n-clicked-algs", "data", allow_duplicate=True),
    ],
    Input("tour-clear-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_tour_selections(n_clicks):
    if not n_clicks:
        return no_update, no_update
    return {}, {"value": 0}
