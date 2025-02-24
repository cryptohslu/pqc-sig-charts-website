import dash_mantine_components as dmc
from dash import html, Output, Input, callback
from dash_iconify import DashIconify


def nist_security_level_filter():
    return html.Div(
        [
            dmc.Stack(
                [
                    dmc.Title("Nist Security Level", order=4),
                    dmc.Group(
                        [
                            dmc.ChipGroup(
                                [
                                    dmc.Chip("1", value="1"),
                                    dmc.Chip("2", value="2"),
                                    dmc.Chip("3", value="3"),
                                    dmc.Chip("4", value="4"),
                                    dmc.Chip("5", value="5"),
                                ],
                                multiple=True,
                                value=["1", "2", "3", "4", "5"],
                                id="nist-security-levels-checkbox",
                            ),
                        ]
                    ),
                ],
                gap="xs",
            )
        ]
    )


def sizes_filter():
    return html.Div(
        [
            dmc.Stack(
                [
                    dmc.Title("Keys & Signatures sizes", order=4),
                    dmc.Title("Public key (bytes)", order=5),
                    dmc.RangeSlider(
                        id="pubkey-slider",
                        min=0,
                        max=5488,
                        value=[0, 5_488],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 32, "label": "32"},
                            {"value": 1000, "label": "1K"},
                            {"value": 2000, "label": "2K"},
                            {"value": 3000, "label": "3K"},
                            {"value": 4000, "label": "4K"},
                            {"value": 5000, "label": "5K"},
                            {"value": 5488, "label": "5488"},
                        ],
                        mb=35,
                    ),
                    dmc.Title("Private key (bytes)", order=5),
                    dmc.RangeSlider(
                        id="privkey-slider",
                        min=0,
                        max=4896,
                        value=[0, 4_896],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 24, "label": "24"},
                            {"value": 1000, "label": "1K"},
                            {"value": 2000, "label": "2K"},
                            {"value": 3000, "label": "3K"},
                            {"value": 4000, "label": "4K"},
                            {"value": 4896, "label": "4896"},
                        ],
                        mb=35,
                    ),
                    dmc.Title("Signature size (bytes)", order=5),
                    dmc.RangeSlider(
                        id="signature-slider",
                        min=0,
                        max=76_298,
                        value=[0, 76_298],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 180, "label": "180"},
                            {"value": 20_000, "label": "10K"},
                            {"value": 40_000, "label": "30K"},
                            {"value": 60_000, "label": "50K"},
                            {"value": 76_298, "label": "76298"},
                        ],
                        mb=35,
                    ),
                ]
            )
        ]
    )


def performance_filters():
    return html.Div(
        [
            dmc.Stack(
                [
                    dmc.Title("Performance", order=4),
                    dmc.Title("Keypair generation", order=5),
                    dmc.RangeSlider(
                        id="keypair-slider",
                        min=0,
                        max=40_000,
                        value=[0, 40_000],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 0, "label": "0"},
                            {"value": 10_000, "label": "10ms"},
                            {"value": 20_000, "label": "20ms"},
                            {"value": 30_000, "label": "30ms"},
                            {"value": 40_000, "label": "40ms"},
                        ],
                        mb=35,
                    ),
                    dmc.Title("Signature creation", order=5),
                    dmc.RangeSlider(
                        id="sign-slider",
                        min=0,
                        max=350_000,
                        value=[0, 350_000],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 0, "label": "0"},
                            {"value": 50_000, "label": "50ms"},
                            {"value": 150_000, "label": "150ms"},
                            {"value": 250_000, "label": "250ms"},
                            {"value": 350_000, "label": "350ms"},
                        ],
                        mb=35,
                    ),
                    dmc.Title("Signature verification", order=5),
                    dmc.RangeSlider(
                        id="verify-slider",
                        min=0,
                        max=2500,
                        value=[0, 2500],
                        updatemode="drag",
                        label=None,
                        marks=[
                            {"value": 0, "label": "0"},
                            {"value": 500, "label": "0.5ms"},
                            {"value": 1000, "label": "1ms"},
                            {"value": 2000, "label": "2ms"},
                            {"value": 2500, "label": "2.5ms"},
                        ],
                        mb=35,
                    ),
                ]
            )
        ]
    )


def create_alg_filters():
    return html.Div(
        [
            dmc.Container(
                size="380px",
                px="xs",
                children=[
                    nist_security_level_filter(),
                    dmc.Space(h="xl"),
                    sizes_filter(),
                    performance_filters(),
                    dmc.Button(
                        "Reset all filters",
                        leftSection=DashIconify(icon="carbon:reset"),
                    ),
                ],
            )
        ]
    )


def create_drawer(data):
    return html.Div(
        [
            dmc.Drawer(
                title="Filter algorithms (44/44)",
                id="filter-drawer",
                padding="md",
                size="425px",
                children=[create_alg_filters()],
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
