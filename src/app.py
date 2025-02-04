from pathlib import Path

from flask import Flask
from dash import (
    Dash,
    _dash_renderer,
    callback,
    dcc,
    Input,
    Output,
    clientside_callback,
)
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd


_dash_renderer._set_react_version("18.2.0")

OQS_VERSION = "0.12.0"
DATASET = "dataset_v2.zst"

df = pd.read_pickle(Path(__file__).resolve().parent.parent / "data" / DATASET)

server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=dmc.styles.ALL)

opts = [["Keygen (μs)", "Keygen"], ["Sign (μs)", "Sign"], ["Verify (μs)", "Verify"]]

app.layout = dmc.MantineProvider(
    defaultColorScheme="dark",
    children=[
        dmc.Container(
            fluid=True,
            style={
                "width": "80%",
                "marginTop": 20,
                "marginBottom": 20,
            },
            children=[
                dmc.Alert(
                    "Demo website using Plotly and Dash",
                    title="Welcome!",
                    color="violet",
                    withCloseButton=True,
                ),
                dmc.Space(h=15),
                dmc.Switch(
                    offLabel=DashIconify(
                        icon="radix-icons:sun",
                        width=15,
                        color=dmc.DEFAULT_THEME["colors"]["yellow"][8],
                    ),
                    onLabel=DashIconify(
                        icon="radix-icons:moon",
                        width=15,
                        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                    ),
                    id="color-scheme-switch",
                    persistence=True,
                    color="grey",
                ),
                dmc.Space(h=30),
                dmc.Title("Benchmarking PQC Signature Algorithms", order=1),
                dmc.Space(h=15),
                dmc.Space(h=15),
                dmc.Text("Select the NIST security level"),
                dmc.Space(h=10),
                dmc.SegmentedControl(
                    id="nist_level",
                    value="3",
                    data=[
                        {"value": "1", "label": "1"},
                        {"value": "2", "label": "2"},
                        {"value": "3", "label": "3"},
                        {"value": "4", "label": "4", "disabled": True},
                        {"value": "5", "label": "5"},
                    ],
                    fullWidth=True,
                    color="violet",
                    transitionDuration=100,
                    transitionTimingFunction="linear",
                ),
                dmc.RadioGroup(
                    id="bench_type",
                    children=dmc.Group([dmc.Radio(l, value=k) for k, l in opts], my=10),
                    value="Verify (μs)",
                    label="Select the benchmark",
                    size="md",
                    my=10,
                ),
                # dmc.BarChart(
                #     id="bar-chart",
                #     h=300,
                #     dataKey="Keygen (μs)",
                #     data=df.loc[2].to_dict(),
                #     series=[{"name": alg} for alg in df.loc[2].index.tolist()],
                #     tickLine="y",
                #     gridAxis="y",
                #     withXAxis=True,
                #     withYAxis=True,
                # ),
                dmc.Space(h=30),
                dcc.Graph(id="keygen_bar"),
                dmc.Space(h=15),
                dmc.Box(
                    [
                        dmc.Button("See raw data", id="collapse-btn", n_clicks=0),
                        dmc.Space(h=10),
                        dmc.Collapse(
                            children=dmc.Table(
                                id="raw_data",
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                data={},
                            ),
                            opened=False,
                            id="collapse-simple",
                        ),
                    ]
                ),
            ],
        )
    ],
)


@app.callback(
    Output("keygen_bar", "figure"),
    [
        Input("nist_level", "value"),
        Input("bench_type", "value"),
        Input("color-scheme-switch", "checked"),
    ],
)
def update_keygen_chart(nist_level, bench_type, color_mode):
    nist_level = int(nist_level)
    fig = px.bar(
        df.loc[nist_level],
        x=df.loc[nist_level].index,
        y=df.loc[nist_level][bench_type],
        range_y=[1, 10**6],
        log_y=True,
        subtitle=f"NIST Level {nist_level}",
        labels={
            "x": "",
        },
        template="plotly_dark" if color_mode else "plotly",
    )
    return fig


@app.callback(Output("raw_data", "data"), Input("nist_level", "value"))
def update_raw_table(nist_level):
    nist_level = int(nist_level)
    data = []
    for i, alg_name in enumerate(df.loc[nist_level].index.tolist()):
        data.append([alg_name] + [f"{_:.1f}" for _ in df.loc[nist_level].values[i]])
    return {
        "caption": f"Raw data generated with liboqs {OQS_VERSION} ({DATASET})",
        "head": ["Algorithm"] + df.loc[2].columns.to_list(),
        "body": data,
    }


@callback(
    Output("collapse-simple", "opened"),
    Input("collapse-btn", "n_clicks"),
)
def update_visibility_raw_table(n):
    if n % 2 == 0:
        return False
    return True


# This is required to update the color mode using the switch button
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');
       return window.dash_clientside.no_update
    }
    """,
    Output("color-scheme-switch", "id"),
    Input("color-scheme-switch", "checked"),
)


if __name__ == "__main__":
    app.run_server(debug=True)
