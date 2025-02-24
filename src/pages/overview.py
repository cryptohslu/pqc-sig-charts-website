from pathlib import Path

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import Input, Output, callback, dcc, html

OQS_VERSION = "0.12.0"
DATASET = "dataset_v2.zst"

df = pd.read_pickle(Path(__file__).resolve().parent.parent.parent / "data" / DATASET)
df = df.reset_index()

selected_algorithms = df["Algorithm"].to_list()
features = [
    "Pubkey (bytes)",
    "Privkey (bytes)",
    "Signature (bytes)",
    "Keygen (μs)",
    "Sign (μs)",
    "Verify (μs)",
]


def generate_radar_chart(alg_name):
    data = []
    raw_data = df[df["Algorithm"] == alg_name][features].squeeze(0)
    for i, val in enumerate(raw_data):
        data.append({"feature": features[i], "value": val})
    return html.Div(
        children=[
            dmc.Stack(
                [
                    dmc.Text(alg_name, c="blue", ta="center"),
                    dmc.RadarChart(
                        id=f"radar_{alg_name}",
                        h=350,
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
            )
        ]
    )


dash.register_page(
    __name__,
    "/",
    title="PQC sigs overview",
    description="Comparative of PQC sigs available in OQS liboqs library.",
)

layout = [
    dcc.Store(id="pqc-data"),
    dmc.SimpleGrid(
        id="grid-overview",
        cols={"base": 1, "sm": 2, "lg": 4},
        spacing="xs",
        children=[generate_radar_chart(alg) for alg in selected_algorithms],
    ),
]


@callback(
    [Output("grid-overview", "children"), Output("website-title", "children")],
    [
        Input("nist-security-levels-checkbox", "value"),
        Input("pubkey-slider", "value"),
        Input("privkey-slider", "value"),
        Input("signature-slider", "value"),
        Input("keypair-slider", "value"),
        Input("sign-slider", "value"),
        Input("verify-slider", "value"),
    ],
    prevent_initial_call=True,
)
def update_selection_algorithms(
    nist_levels, pubkey, privkey, sig, keypair, sign, verify
):
    n_algs_total = df.shape[0]
    try:
        # fmt: off
        tmp = pd.concat([df[df["NIST"] == int(l)] for l in nist_levels])
        tmp = tmp[(tmp["Pubkey (bytes)"] >= int(pubkey[0])) & (tmp["Pubkey (bytes)"] <= int(pubkey[1]))]
        tmp = tmp[(tmp["Privkey (bytes)"] >= int(privkey[0])) & (tmp["Privkey (bytes)"] <= int(privkey[1]))]
        tmp = tmp[(tmp["Signature (bytes)"] >= int(sig[0])) & (tmp["Signature (bytes)"] <= int(sig[1]))]
        tmp = tmp[(tmp["Keygen (μs)"] >= int(keypair[0])) & (tmp["Keygen (μs)"] <= int(keypair[1]))]
        tmp = tmp[(tmp["Sign (μs)"] >= int(sign[0])) & (tmp["Sign (μs)"] <= int(sign[1]))]
        tmp = tmp[(tmp["Verify (μs)"] >= int(verify[0])) & (tmp["Verify (μs)"] <= int(verify[1]))]
        # fmt: on
    except Exception:

        return [], f"PQC sigs chart (0 / {n_algs_total})"
    selected_algorithms = tmp["Algorithm"].to_list()
    return [
        generate_radar_chart(alg) for alg in selected_algorithms
    ], f"PQC sigs chart ({len(selected_algorithms)} / {n_algs_total})"
