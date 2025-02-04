from pathlib import Path

import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, _dash_renderer, callback, clientside_callback, dcc
from dash_iconify import DashIconify
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

_dash_renderer._set_react_version("18.2.0")
colors = ["#ff6b6b", "#339af0", "#51cf66", "#fcc419", "#cc5de8"]

OQS_VERSION = "0.12.0"
DATASET = "dataset_v2.zst"

df = pd.read_pickle(Path(__file__).resolve().parent.parent / "data" / DATASET)

data_radar_nist_1_2 = []
data_radar_nist_3 = []
data_radar_nist_5 = []

for feature in df.loc[[1, 2]].columns:
    data_radar_nist_1_2.append(
        {"feature": feature}
        | df.loc[1].loc[:, feature].to_dict()
        | df.loc[2].loc[:, feature].to_dict()
    )

for feature in df.loc[3].columns:
    data_radar_nist_3.append({"feature": feature} | df.loc[3].loc[:, feature].to_dict())

for feature in df.loc[5].columns:
    data_radar_nist_5.append({"feature": feature} | df.loc[5].loc[:, feature].to_dict())

server = Flask(__name__)
server.wsgi_app = ProxyFix(server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
server.config["APPLICATION_ROOT"] = "/sig-charts"

app = Dash(
    __name__,
    server=server,
    external_stylesheets=dmc.styles.ALL,
    url_base_pathname="/sig-charts/",
)

opts = [["Keygen (μs)", "Keygen"], ["Sign (μs)", "Sign"], ["Verify (μs)", "Verify"]]

data = [
    {"product": "Apples", "sales": 120},
    {"product": "Oranges", "sales": 98},
    {"product": "Tomatoes", "sales": 86},
    {"product": "Grapes", "sales": 99},
    {"product": "Bananas", "sales": 85},
    {"product": "Lemons", "sales": 65},
]

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
                dmc.Group(
                    grow=True,
                    preventGrowOverflow=False,
                    wrap="nowrap",
                    children=[
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "NIST Security Level 1 & 2", size="md", ta="center"
                                ),
                                dmc.RadarChart(
                                    id="radar_nist_1_2",
                                    h=350,
                                    data=data_radar_nist_1_2,
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
                                        "isAnimationActive": True,
                                    },
                                    withLegend=True,
                                    series=[],
                                ),
                                dmc.Center(
                                    [
                                        dmc.MultiSelect(
                                            id="multi-select-nist-1-2",
                                            description="You can select a maximum of 5 algs.",
                                            value=[
                                                "ML-DSA-44",
                                                "Falcon-512",
                                                "SPHINCS+-SHA2-128s-simple",
                                            ],
                                            maxValues=5,
                                            data=[
                                                {"value": _, "label": _}
                                                for _ in df.loc[1].index.tolist()
                                                + df.loc[2].index.tolist()
                                            ],
                                            w=400,
                                            mb=10,
                                        ),
                                    ]
                                ),
                            ],
                            align="stretch",
                            gap="sm",
                        ),
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "NIST Security Level 3", size="md", ta="center"
                                ),
                                dmc.RadarChart(
                                    id="radar_nist_3",
                                    h=350,
                                    data=data_radar_nist_3,
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
                                        "isAnimationActive": True,
                                    },
                                    withLegend=True,
                                    series=[],
                                ),
                                dmc.Center(
                                    [
                                        dmc.MultiSelect(
                                            id="multi-select-nist-3",
                                            description="You can select a maximum of 5 algs.",
                                            value=[
                                                "ML-DSA-65",
                                                "MAYO-3",
                                                "SPHINCS+-SHA2-192s-simple",
                                            ],
                                            maxValues=5,
                                            data=[
                                                {"value": _, "label": _}
                                                for _ in df.loc[3].index.tolist()
                                            ],
                                            w=400,
                                            mb=10,
                                        ),
                                    ]
                                ),
                            ],
                            align="stretch",
                            gap="sm",
                        ),
                        dmc.Stack(
                            [
                                dmc.Text(
                                    "NIST Security Level 5", size="md", ta="center"
                                ),
                                dmc.RadarChart(
                                    id="radar_nist_5",
                                    h=350,
                                    data=data_radar_nist_5,
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
                                        "isAnimationActive": True,
                                    },
                                    withLegend=True,
                                    series=[],
                                ),
                                dmc.Center(
                                    [
                                        dmc.MultiSelect(
                                            id="multi-select-nist-5",
                                            description="You can select a maximum of 5 algs.",
                                            value=[
                                                "ML-DSA-87",
                                                "FALCON-1024",
                                                "SPHINCS+-SHA2-256s-simple",
                                            ],
                                            maxValues=5,
                                            data=[
                                                {"value": _, "label": _}
                                                for _ in df.loc[5].index.tolist()
                                            ],
                                            w=400,
                                            mb=10,
                                        ),
                                    ]
                                ),
                            ],
                            align="stretch",
                            gap="sm",
                        ),
                    ],
                ),
                dmc.Space(h=30),
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


@callback(
    Output("radar_nist_1_2", "series"),
    Input("multi-select-nist-1-2", "value"),
)
def update_radar_nist_1_2(algs):
    d = []
    for i, alg in enumerate(algs):
        c = colors[i]
        d.append(
            {"name": alg, "color": c, "opacity": 0.25},
        )
    return d


@callback(
    Output("radar_nist_3", "series"),
    Input("multi-select-nist-3", "value"),
)
def update_radar_nist_3(algs):
    d = []
    for i, alg in enumerate(algs):
        c = colors[i]
        d.append(
            {"name": alg, "color": c, "opacity": 0.25},
        )
    return d


@callback(
    Output("radar_nist_5", "series"),
    Input("multi-select-nist-5", "value"),
)
def update_radar_nist_5(algs):
    d = []
    for i, alg in enumerate(algs):
        c = colors[i]
        d.append(
            {"name": alg, "color": c, "opacity": 0.25},
        )
    return d


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
