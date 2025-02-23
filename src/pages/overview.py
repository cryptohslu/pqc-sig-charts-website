from pathlib import Path
import pandas as pd
import dash
import dash_mantine_components as dmc
from dash import html


OQS_VERSION = "0.12.0"
DATASET = "dataset_v2.zst"

df = pd.read_pickle(Path(__file__).resolve().parent.parent.parent / "data" / DATASET)
df.index = df.index.droplevel(0)
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
    dmc.SimpleGrid(
        cols={"base": 1, "sm": 2, "lg": 4},
        spacing="xs",
        children=[generate_radar_chart(alg) for alg in selected_algorithms],
    )
]
