import dash_mantine_components as dmc
import numpy as np
from dash import ALL, Input, Output, State, callback, html
from dash_iconify import DashIconify

from components.dataset import DATASETS, DEFAULT_DATASET


def nist_security_level_filter():
    return html.Div(
        [
            dmc.Stack(
                [
                    dmc.Title("NIST Security Level", order=4),
                    dmc.Group(
                        [
                            dmc.ChipGroup(
                                [
                                    dmc.Chip("0", value="0", size="xs"),
                                    dmc.Chip("1", value="1", size="xs"),
                                    dmc.Chip("2", value="2", size="xs"),
                                    dmc.Chip("3", value="3", size="xs"),
                                    dmc.Chip("4", value="4", size="xs"),
                                    dmc.Chip("5", value="5", size="xs"),
                                ],
                                multiple=True,
                                value=["0", "1", "2", "3", "4", "5"],
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
                        min=np.log10(32),
                        max=np.log10(3_000_000),
                        step=0.1,
                        minRange=1,
                        value=(np.log10(32), np.log10(3_000_000)),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": np.log10(32), "label": "32"},
                            {"value": np.log10(256), "label": "256"},
                            {"value": np.log10(1_000), "label": "1K"},
                            {"value": np.log10(5_000), "label": "5K"},
                            {"value": np.log10(100_000), "label": "100K"},
                            {"value": np.log10(3_000_000), "label": "3M"},
                        ],
                        mb=20,
                    ),
                    dmc.Title("Private key (bytes)", order=5),
                    dmc.RangeSlider(
                        id="privkey-slider",
                        min=np.log10(24),
                        max=np.log10(2_500_000),
                        step=0.1,
                        minRange=1,
                        value=(np.log10(24), np.log10(2_436_704)),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": np.log10(24), "label": "24"},
                            {"value": np.log10(256), "label": "256"},
                            {"value": np.log10(1_000), "label": "1K"},
                            {"value": np.log10(5_000), "label": "5K"},
                            {"value": np.log10(100_000), "label": "100K"},
                            {"value": np.log10(2_500_000), "label": "2.5M"},
                        ],
                        mb=20,
                    ),
                    dmc.Title("Signature size (bytes)", order=5),
                    dmc.RangeSlider(
                        id="signature-slider",
                        min=64,
                        max=75_000,
                        value=(64, 75_000),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": 64, "label": "64"},
                            {"value": 20_000, "label": "10K"},
                            {"value": 40_000, "label": "30K"},
                            {"value": 60_000, "label": "50K"},
                            {"value": 75_000, "label": "75K"},
                        ],
                        mb=20,
                    ),
                ],
                gap="xs",
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
                        max=np.log10(10 * 60 * 60 * 1e6),
                        step=0.1,
                        minRange=1,
                        value=(0, np.log10(10 * 60 * 60 * 1e6)),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": np.log10(1), "label": "1μs"},
                            {"value": np.log10(1e3), "label": "1ms"},
                            {"value": np.log10(1e6), "label": "1s"},
                            {"value": np.log10(60 * 1e6), "label": "1min"},
                            {"value": np.log10(60 * 60 * 1e6), "label": "1h"},
                            {"value": np.log10(10 * 60 * 60 * 1e6), "label": "10h"},
                        ],
                        mb=20,
                    ),
                    dmc.Title("Signature creation", order=5),
                    dmc.RangeSlider(
                        id="sign-slider",
                        min=0,
                        max=np.log10(10 * 60 * 60 * 1e6),
                        step=0.1,
                        minRange=1,
                        value=(0, np.log10(10 * 60 * 60 * 1e6)),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": np.log10(1), "label": "1μs"},
                            {"value": np.log10(1e3), "label": "1ms"},
                            {"value": np.log10(1e6), "label": "1s"},
                            {"value": np.log10(60 * 1e6), "label": "1min"},
                            {"value": np.log10(60 * 60 * 1e6), "label": "1h"},
                            {"value": np.log10(10 * 60 * 60 * 1e6), "label": "10h"},
                        ],
                        mb=20,
                    ),
                    dmc.Title("Signature verification", order=5),
                    dmc.RangeSlider(
                        id="verify-slider",
                        min=0,
                        max=6,
                        step=0.1,
                        minRange=1,
                        value=(0, 6),
                        updatemode="mouseup",
                        label=None,
                        marks=[
                            {"value": 0, "label": "1μs"},
                            {"value": 3, "label": "1ms"},
                            {"value": 6, "label": "1s"},
                        ],
                        mb=40,
                    ),
                ],
                gap="xs",
            )
        ]
    )


def create_alg_filters():
    return html.Div(
        [
            dmc.Container(
                size="350px",
                px="xs",
                children=[
                    dmc.TextInput(
                        id="alg-search",
                        placeholder="Search algorithms...",
                        leftSection=DashIconify(icon="tabler:search"),
                        debounce=300,
                    ),
                    dmc.Space(h="sm"),
                    nist_security_level_filter(),
                    dmc.Space(h="sm"),
                    sizes_filter(),
                    dmc.Space(h="sm"),
                    performance_filters(),
                    dmc.Divider(my="xs"),
                    dmc.Select(
                        id="dataset-selector",
                        label="Dataset",
                        data=[{"value": k, "label": v} for k, v in DATASETS.items()],
                        value=DEFAULT_DATASET,
                        allowDeselect=False,
                        checkIconPosition="right",
                        leftSectionPointerEvents="none",
                        leftSection=DashIconify(icon="material-symbols:dataset"),
                    ),
                    dmc.Space(h="xs"),
                    dmc.Button(
                        "Reset All",
                        id="reset-button",
                        leftSection=DashIconify(icon="tabler:zoom-reset"),
                    ),
                ],
            )
        ]
    )


def create_navbar(data):
    return dmc.AppShellNavbar(
        id="navbar",
        children=[
            dmc.ScrollArea(
                [
                    create_alg_filters(),
                ],
                type="scroll",
                w=355,
                h=1000,
            )
        ],
        p="xs",
    )


@callback(
    [
        Output("alg-search", "value"),
        Output("nist-security-levels-checkbox", "value"),
        Output("pubkey-slider", "value"),
        Output("privkey-slider", "value"),
        Output("signature-slider", "value"),
        Output("keypair-slider", "value"),
        Output("sign-slider", "value"),
        Output("verify-slider", "value"),
        Output({"type": "checkbox-alg", "index": ALL}, "checked"),
        Output("dataset-selector", "value"),
    ],
    Input("reset-button", "n_clicks"),
    State({"type": "checkbox-alg", "index": ALL}, "checked"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks, algs):
    return (
        "",
        ("0", "1", "2", "3", "4", "5"),
        (np.log10(32), np.log10(3_000_000)),
        (np.log10(24), np.log10(2_500_000)),
        (0, 75_000),
        (0, np.log10(10 * 60 * 60 * 1e6)),
        (0, np.log10(10 * 60 * 60 * 1e6)),
        (0, 6),
        len(algs) * [False],
        DEFAULT_DATASET,
    )
