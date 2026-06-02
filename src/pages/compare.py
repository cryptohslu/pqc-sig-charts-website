import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import Input, Output, State, callback, clientside_callback, html, no_update

from components.dataset import ALL_DATA, DATASETS, DEFAULT_DATASET, FEATURES

COLORS = ["#ff6b6b", "#339af0", "#51cf66", "#fcc419", "#cc5de8"]


def _fmt(value, decimals=None):
    if decimals is not None:
        s = f"{value:,.{decimals}f}"
    else:
        s = f"{int(value):,}"
    return s.replace(",", "\N{NARROW NO-BREAK SPACE}")

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
    title="PQC Digital Signatures",
    description="Comparative of PQC sigs available in OQS liboqs library.",
)

layout = []


def generate_table(algs, df, table_id="compare-table"):
    data = []
    tmp = pd.concat([df[df["Algorithm"] == alg_name] for alg_name in algs if algs[alg_name]])
    for i, row in tmp.iterrows():
        alg_name = row["Algorithm"]
        nist_level = row["NIST Security Level"]
        sizes = [_fmt(row.values[i]) for i in range(2, 5)]
        times = [_fmt(row.values[i], decimals=1) for i in range(5, 8)]
        data.append([alg_name, nist_level] + sizes + times)

    return dmc.Container(
        id=table_id,
        children=[
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                data={
                    "head": [
                        "Algorithm",
                        "NIST Security Level",
                        "Public key size (bytes)",
                        "Private key size (bytes)",
                        "Signature size (bytes)",
                        "Key generation time (μs)",
                        "Signing time (μs)",
                        "Verififcation time (μs)",
                    ],
                    "body": data,
                },
            )
        ],
        size="90%",
    )


def generate_radar(algs, df, chart_id="compare-radar"):
    alg_names_enabled = [alg for alg in algs if algs[alg]]
    alg_names_present = [alg for alg in alg_names_enabled if not df[df["Algorithm"] == alg].empty]

    data = []
    if alg_names_present:
        tmp = pd.concat([df[df["Algorithm"] == alg_name] for alg_name in alg_names_present])
        for feature in FEATURES:
            serie = {"feature": feature}
            for _, row in tmp.iterrows():
                serie[row["Algorithm"]] = row[feature]
            data.append(serie)

    series = []
    for count, alg in enumerate(alg_names_enabled):
        if alg in alg_names_present:
            series.append({"name": alg, "color": COLORS[count], "opacity": 0.25})

    return dmc.RadarChart(
        id=chart_id,
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


def generate_radar_pair(algs, df_base, df_compare, base_label, compare_label):
    def label(prefix, name):
        return dmc.Text([html.B(f"{prefix}: "), name], size="xs", c="dimmed", ta="center", mt="xs")

    return dmc.Group(
        id="compare-radar-pair",
        justify="center",
        align="flex-start",
        wrap="wrap",
        gap="xl",
        children=[
            dmc.Stack(
                [generate_radar(algs, df_base), label("Base", base_label)],
                align="center",
                gap=0,
            ),
            dmc.Stack(
                [generate_radar(algs, df_compare, chart_id="compare-radar-2"), label("Comparison", compare_label)],
                align="center",
                gap=0,
            ),
        ],
    )


def generate_merged_table(algs, df_base, df_compare, base_label, compare_label):
    _TIMING_COLS = ["Keygen (μs)", "Sign (μs)", "Verify (μs)"]
    alg_names = [alg for alg in algs if algs[alg]]

    rows = []
    for alg_name in alg_names:
        base_row = df_base[df_base["Algorithm"] == alg_name].iloc[0]
        compare_rows = df_compare[df_compare["Algorithm"] == alg_name]
        missing_in_compare = compare_rows.empty

        cells = [
            dmc.TableTd(alg_name),
            dmc.TableTd(str(base_row["NIST Security Level"])),
            dmc.TableTd(_fmt(base_row["Pubkey (bytes)"])),
            dmc.TableTd(_fmt(base_row["Privkey (bytes)"])),
            dmc.TableTd(_fmt(base_row["Signature (bytes)"])),
        ]
        for col in _TIMING_COLS:
            base_val = float(base_row[col])
            cells.append(dmc.TableTd(_fmt(base_val, decimals=1)))
            if missing_in_compare:
                cells.append(dmc.TableTd("—"))
            else:
                compare_val = float(compare_rows.iloc[0][col])
                diff = ((compare_val - base_val) / base_val * 100) if base_val != 0 else 0
                diff_color = "var(--mantine-color-green-6)" if diff < 0 else "var(--mantine-color-red-6)"
                diff_str = f"({diff:+.1f}%)" if abs(diff) < 1 else f"({diff:+.0f}%)"
                cells.append(
                    dmc.TableTd(
                        [
                            _fmt(compare_val, decimals=1) + " ",
                            html.Span(
                                diff_str,
                                style={"color": diff_color, "fontSize": "0.85em", "whiteSpace": "nowrap"},
                            ),
                        ]
                    )
                )
        rows.append(dmc.TableTr(cells))

    thead = dmc.TableThead(
        [
            dmc.TableTr(
                [
                    dmc.TableTh("Algorithm", tableProps={"rowSpan": 2}),
                    dmc.TableTh("NIST Security Level", tableProps={"rowSpan": 2}),
                    dmc.TableTh("Public key size (bytes)", tableProps={"rowSpan": 2}),
                    dmc.TableTh("Private key size (bytes)", tableProps={"rowSpan": 2}),
                    dmc.TableTh("Signature size (bytes)", tableProps={"rowSpan": 2}),
                    dmc.TableTh("Key generation time (μs)", ta="center", tableProps={"colSpan": 2}),
                    dmc.TableTh("Signing time (μs)", ta="center", tableProps={"colSpan": 2}),
                    dmc.TableTh("Verififcation time (μs)", ta="center", tableProps={"colSpan": 2}),
                ]
            ),
            dmc.TableTr(
                [
                    dmc.TableTh("Base"),
                    dmc.TableTh("Comparison"),
                    dmc.TableTh("Base"),
                    dmc.TableTh("Comparison"),
                    dmc.TableTh("Base"),
                    dmc.TableTh("Comparison"),
                ]
            ),
        ]
    )

    legend = dmc.Text(
        [html.B("Base: "), base_label, " | ", html.B("Comparison: "), compare_label],
        size="xs",
        c="dimmed",
        ta="center",
        mt="xs",
    )

    return dmc.Container(
        id="compare-table",
        children=[
            dmc.TableScrollContainer(
                dmc.Table(
                    striped=True,
                    highlightOnHover=True,
                    withTableBorder=True,
                    withColumnBorders=True,
                    children=[thead, dmc.TableTbody(rows)],
                ),
                minWidth=800,
            ),
            legend,
        ],
        size="95%",
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
        Input("compare-dataset-selector", "value"),
    ],
    State("n-clicked-algs", "data"),
    prevent_initial_call=True,
)
def update_comparison(clicked_algs, url, selected_dataset, compare_dataset, n_clicked):
    if url != "/sig-charts/compare/":
        return [], no_update

    if not clicked_algs or not any(clicked_algs.values()):
        return no_update

    base_dataset = selected_dataset or DEFAULT_DATASET
    df_base = ALL_DATA[base_dataset][_COLUMNS]

    if compare_dataset:
        df_compare = ALL_DATA[compare_dataset][_COLUMNS]
        base_label = DATASETS[base_dataset]
        compare_label = DATASETS[compare_dataset]
        return (
            [
                generate_radar_pair(clicked_algs, df_base, df_compare, base_label, compare_label),
                generate_merged_table(clicked_algs, df_base, df_compare, base_label, compare_label),
            ],
            "PQC Digital Signatures",
        )

    return (
        [
            generate_radar(clicked_algs, df_base),
            generate_table(clicked_algs, df_base),
        ],
        "PQC Digital Signatures",
    )
