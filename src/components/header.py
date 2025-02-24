import dash_mantine_components as dmc
from dash import Input, Output, clientside_callback
from dash_iconify import DashIconify

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
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
            dmc.Stack(
                justify="center",
                h=70,
                children=dmc.Grid(
                    justify="space-between",
                    children=[
                        dmc.GridCol(
                            dmc.Group(
                                [
                                    dmc.Burger(
                                        id="mobile-burger",
                                        size="sm",
                                        hiddenFrom="sm",
                                        opened=False,
                                    ),
                                    dmc.Burger(
                                        id="desktop-burger",
                                        size="sm",
                                        visibleFrom="sm",
                                        opened=True,
                                    ),
                                    dmc.Anchor(
                                        "PQC sigs chart",
                                        size="xl",
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
                                    dmc.Button("Compare", variant="subtle"),
                                    dmc.Button("HSLU", variant="subtle"),
                                    dmc.Button(
                                        "Applied Cyber Security Research Lab",
                                        variant="subtle",
                                    ),
                                    theme_toggle,
                                ],
                            ),
                        ),
                    ],
                ),
            )
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
