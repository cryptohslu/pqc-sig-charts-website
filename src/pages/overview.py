from pathlib import Path

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import ALL, Input, Output, State, callback, dcc, html, no_update

from components.dataset import FEATURES
from components.dataset import data as df

df = df.reset_index()

selected_algs = {alg: True for alg in df["Algorithm"].to_list()}
clicked_algs = {alg: False for alg in df["Algorithm"].to_list()}


selected = 0


def generate_radar_chart(alg_name):
    data = []
    raw_data = df[df["Algorithm"] == alg_name][FEATURES].squeeze(0)
    for i, val in enumerate(raw_data):
        data.append({"feature": FEATURES[i].split("(")[0].strip(), "value": val})
    return html.Div(
        children=[
            dmc.Stack(
                [
                    dmc.Group(
                        [
                            dmc.Checkbox(
                                id={
                                    "type": "checkbox-alg",
                                    "index": f"checkbox-{alg_name}",
                                },
                                checked=False,
                                size="xs",
                                variant="filled",
                                label=dmc.Text(alg_name, ta="center"),
                            ),
                        ],
                        justify="center",
                    ),
                    dmc.RadarChart(
                        id=f"radar_{alg_name}",
                        h=350,
                        w=350,
                        data=data,
                        dataKey="feature",
                        withPolarGrid=True,
                        withPolarAngleAxis=True,
                        withPolarRadiusAxis=True,
                        polarRadiusAxisProps={
                            "angle": 60,
                            "scale": "log",
                            "domain": [1, 10**6],
                        },
                        radarProps={
                            "isAnimationActive": False,
                        },
                        series=[{"name": "value", "color": "blue.4", "opacity": 0.5}],
                    ),
                ],
                gap="xs",
                align="center",
            ),
        ]
    )


dash.register_page(
    __name__,
    "/",
    title="PQC sigs overview",
    description="Comparative of PQC sigs available in OQS liboqs library.",
)

layout = [
    dmc.SimpleGrid(
        id="content",
        type="container",
        cols={
            "base": 1,
            "700px": 2,
            "1050px": 3,
            "1400px": 4,
            "1750px": 5,
            "2100px": 6,
        },
        spacing="xs",
        children=[generate_radar_chart(alg) for alg in df["Algorithm"].to_list()],
    ),
]


@callback(
    [
        Output("selected-algs", "data"),
        Output("n-selected-algs", "data"),
    ],
    [
        Input("nist-security-levels-checkbox", "value"),
        Input("pubkey-slider", "value"),
        Input("privkey-slider", "value"),
        Input("signature-slider", "value"),
        Input("keypair-slider", "value"),
        Input("sign-slider", "value"),
        Input("verify-slider", "value"),
    ],
)
def update_filtered_algorithms(
    nist_levels, pubkey, privkey, sig, keypair, sign, verify
):
    all_algs = df["Algorithm"].to_list()
    # fmt: off
    try:
        tmp = pd.concat([df[df["NIST"] == int(l)] for l in nist_levels])
    except ValueError:
        return {alg: False for alg in all_algs}
    tmp = tmp[(tmp["Pubkey (bytes)"] >= int(pubkey[0])) & (tmp["Pubkey (bytes)"] <= int(pubkey[1]))]
    tmp = tmp[(tmp["Privkey (bytes)"] >= int(privkey[0])) & (tmp["Privkey (bytes)"] <= int(privkey[1]))]
    tmp = tmp[(tmp["Signature (bytes)"] >= int(sig[0])) & (tmp["Signature (bytes)"] <= int(sig[1]))]
    tmp = tmp[(tmp["Keygen (μs)"] >= int(keypair[0])) & (tmp["Keygen (μs)"] <= int(keypair[1]))]
    tmp = tmp[(tmp["Sign (μs)"] >= int(sign[0])) & (tmp["Sign (μs)"] <= int(sign[1]))]
    tmp = tmp[(tmp["Verify (μs)"] >= int(verify[0])) & (tmp["Verify (μs)"] <= int(verify[1]))]
    # fmt: on

    selected = tmp["Algorithm"].to_list()
    selected_algs = {}
    for alg in all_algs:
        if alg in selected:
            selected_algs[alg] = True
        else:
            selected_algs[alg] = False
    return selected_algs, {"value": len(selected)}


@callback(
    [
        Output("content", "children", allow_duplicate=True),
        Output("website-title", "children"),
    ],
    [
        Input("selected-algs", "data"),
        Input("n-selected-algs", "data"),
    ],
    State("url", "pathname"),
    prevent_initial_call=True,
)
def update_shown_charts(algs, n_algs, url):
    if url != "/sig-charts/":
        return no_update

    n_algs_total = df.shape[0]
    charts = []
    for alg_name in algs:
        if algs[alg_name]:
            charts.append(generate_radar_chart(alg_name))

    return (
        charts,
        f"PQC sigs chart ({n_algs["value"]} / {n_algs_total})",
    )


@callback(
    Output("clicked-algs", "data"),
    Input({"type": "checkbox-alg", "index": ALL}, "checked"),
    [State({"type": "checkbox-alg", "index": ALL}, "id"), State("url", "pathname")],
    prevent_initial_call=True,
)
def update_clicked_algorithms(values, ids, url):
    if url == "/sig-charts/compare/":
        return no_update

    clicked_algs = {}
    for i, id_ in enumerate(ids):
        alg_name = "-".join(id_["index"].split("-")[1:])
        if values[i]:
            clicked_algs[alg_name] = True
        else:
            clicked_algs[alg_name] = False
    return clicked_algs


@callback(
    [
        Output("compare-button", "children"),
        Output("n-clicked-algs", "data"),
    ],
    Input("clicked-algs", "data"),
    prevent_initial_call=True,
)
def update_compare_selection(clicked):
    if clicked is None:
        return no_update
    n_clicked = 0
    for alg in clicked:
        if clicked[alg]:
            n_clicked += 1
    return f"Compare ({n_clicked})", {"value": n_clicked}


@callback(
    Output({"type": "checkbox-alg", "index": ALL}, "disabled"),
    [Input("n-clicked-algs", "data")],
    [
        State({"type": "checkbox-alg", "index": ALL}, "checked"),
        State("n-selected-algs", "data"),
    ],
    prevent_initial_call=True,
)
def disable_checkboxes(clicked, checked, selected):
    selected = selected["value"]
    if clicked["value"] < 5:
        return selected * [False]

    disabled_list = selected * [False]
    for i, id_ in enumerate(checked):
        if not id_:
            disabled_list[i] = True

    return disabled_list
