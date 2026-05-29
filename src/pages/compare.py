import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import Input, Output, State, callback, clientside_callback, no_update

from components.dataset import ALL_DATA, DEFAULT_DATASET, FEATURES

COLORS = ["#ff6b6b", "#339af0", "#51cf66", "#fcc419", "#cc5de8"]

_COLUMNS = [
    "Algorithm",
    "NIST Security Level",
    "Pubkey (bytes)",
    "Privkey (bytes)",
    "Signature (bytes)",
    "Keygen (μs)",
    "Sign (μs)",
    "Verify (μs)",
]

dash.register_page(
    __name__,
    "/compare",
    title="PQC DS",
    description="Comparative of PQC sigs available in OQS liboqs library.",
)

layout = []


def generate_table(algs, df):
    data = []
    tmp = pd.concat([df[df["Algorithm"] == alg_name] for alg_name in algs if algs[alg_name]])
    for i, row in tmp.iterrows():
        alg_name = row["Algorithm"]
        nist_level = row["NIST Security Level"]
        sizes = [f"{row.values[i]}" for i in range(2, 5)]
        times = [f"{row.values[i]:.1f}" for i in range(5, 8)]
        data.append([alg_name, nist_level] + sizes + times)

    return dmc.Container(
        [
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                data={
                    "head": df.columns.to_list(),
                    "body": data,
                },
            )
        ],
        size="90%",
    )


def generate_radar(algs, df):
    data = []
    tmp = pd.concat([df[df["Algorithm"] == alg_name] for alg_name in algs if algs[alg_name]])
    for feature in FEATURES:
        serie = {"feature": feature}
        for i, row in tmp.iterrows():
            serie[row["Algorithm"]] = row[feature]
        data.append(serie)

    series = []
    count = 0
    for alg in algs:
        if algs[alg]:
            series.append({"name": alg, "color": COLORS[count], "opacity": 0.25})
            count += 1

    return dmc.RadarChart(
        w=600,
        h=600,
        data=data,
        dataKey="feature",
        withPolarGrid=True,
        withPolarAngleAxis=True,
        withPolarRadiusAxis=True,
        polarRadiusAxisProps={
            "angle": 90,
            "scale": "log",
            "domain": [1, 10**9],
            "ticks": [10**i for i in range(9)],
        },
        radarProps={
            "isAnimationActive": True,
        },
        withLegend=True,
        series=series,
    )


clientside_callback(
    """
    function(children) {
        var sups = {2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', 10: '¹⁰'};
        function fmt() {
            document.querySelectorAll('.recharts-polar-radius-axis tspan').forEach(function(el) {
                var val = parseFloat(el.textContent);
                if (isNaN(val) || val <= 10) return;
                var exp = Math.round(Math.log10(val));
                if (sups[exp]) el.textContent = '10' + sups[exp];
            });
        }
        requestAnimationFrame(fmt);
        return window.dash_clientside.no_update;
    }
    """,
    Output("content-compare", "className"),
    Input("content-compare", "children"),
)


@callback(
    [
        Output("content-compare", "children"),
        Output("website-title", "children", allow_duplicate=True),
    ],
    [
        Input("clicked-algs", "data"),
        Input("url", "pathname"),
        Input("dataset-selector", "value"),
    ],
    State("n-clicked-algs", "data"),
    prevent_initial_call=True,
)
def update_comparison(clicked_algs, url, selected_dataset, n_clicked):
    if url != "/sig-charts/compare/":
        return [], no_update

    if not clicked_algs or not any(clicked_algs.values()):
        return no_update

    df = ALL_DATA[selected_dataset or DEFAULT_DATASET][_COLUMNS]
    return (
        [
            generate_radar(clicked_algs, df),
            generate_table(clicked_algs, df),
        ],
        "PQC Signatures",
    )
