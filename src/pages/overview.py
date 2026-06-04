import dash
import dash_mantine_components as dmc
from dash import (
    ALL,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    html,
    no_update,
)

from components.dataset import ALL_DATA, DEFAULT_DATASET, FEATURES

_FEATURE_LABELS = [f.split("(")[0].strip() for f in FEATURES]

_CHART_DATA: dict[str, dict[str, list]] = {}
for _dataset, _df in ALL_DATA.items():
    _CHART_DATA[_dataset] = {
        row["Algorithm"]: [{"feature": _FEATURE_LABELS[i], "value": row[feat]} for i, feat in enumerate(FEATURES)]
        for _, row in _df.iterrows()
    }


def add_soft_break(s: str) -> str:
    # U+200B = zero-width space (soft wrap opportunity)
    return s.replace("_", "_\u200b")


def generate_radar_chart(alg_name, dataset, clicked_algs=None):
    data = _CHART_DATA[dataset][alg_name]
    is_selected = bool(clicked_algs and clicked_algs.get(alg_name))
    return html.Div(
        id={
            "type": "radar-clickable",
            "index": f"radar_{alg_name}",
        },
        n_clicks=0,
        className="radar-card radar-card--selected" if is_selected else "radar-card",
        style={"width": "250px", "padding": "6px 4px 0 4px"},
        children=[
            dmc.Text(
                add_soft_break(alg_name),
                ta="center",
                fw=700,
                style={
                    "fontSize": "10pt",
                    "maxWidth": "240px",
                    "whiteSpace": "normal",
                    "overflowWrap": "anywhere",
                    "wordBreak": "break-word",
                    "lineHeight": "1.1",
                    "display": "-webkit-box",
                    "WebkitBoxOrient": "vertical",
                    "WebkitLineClamp": 2,
                    "overflow": "hidden",
                    "marginBottom": "2px",
                },
            ),
            dmc.RadarChart(
                id={
                    "type": "radar-chart",
                    "index": f"radar_{alg_name}",
                },
                h=350,
                w=350,
                data=data,
                dataKey="feature",
                withPolarGrid=True,
                withPolarAngleAxis=True,
                withPolarRadiusAxis=True,
                polarRadiusAxisProps={
                    "angle": 90,
                    "scale": "log",
                    "domain": [1, 10**11],
                    "ticks": [1, 10**2, 10**4, 10**6, 10**8, 10**10],
                    "tick": False,
                },
                radarProps={
                    "isAnimationActive": False,
                },
                radarChartProps={
                    "margin": {
                        "top": 0,
                        "right": 0,
                        "bottom": 0,
                        "left": 0,
                    },
                    "outerRadius": "40%",
                },
                polarGridProps={
                    "outerRadius": -10,
                },
                series=[{"name": "value", "color": "blue.4", "opacity": 0.5}],
                style={"margin": "-75px"},
            ),
        ],
    )


dash.register_page(
    __name__,
    "/",
    title="PQC Digital Signatures",
    description="Comparative of PQC sigs available in OQS liboqs library.",
)

layout = []


@callback(
    Output("selected-algs", "data"),
    [
        Input("alg-search", "value"),
        Input("nist-security-levels-checkbox", "value"),
        Input("pubkey-slider", "value"),
        Input("privkey-slider", "value"),
        Input("signature-slider", "value"),
        Input("keypair-slider", "value"),
        Input("sign-slider", "value"),
        Input("verify-slider", "value"),
        Input("dataset-selector", "value"),
    ],
)
def update_filtered_algorithms(search, nist_levels, pubkey, privkey, sig, keypair, sign, verify, selected_dataset):
    df = ALL_DATA[selected_dataset or DEFAULT_DATASET]

    if not nist_levels:
        return []

    mask = (
        df["NIST Security Level"].isin([int(l) for l in nist_levels])
        & (df["Pubkey (bytes)"] >= int(10 ** pubkey[0]))
        & (df["Pubkey (bytes)"] <= int(10 ** pubkey[1]))
        & (df["Privkey (bytes)"] >= int(10 ** privkey[0]))
        & (df["Privkey (bytes)"] <= int(10 ** privkey[1]))
        & (df["Signature (bytes)"] >= int(sig[0]))
        & (df["Signature (bytes)"] <= int(sig[1]))
        & (df["Keygen (μs)"] >= 10 ** keypair[0])
        & (df["Keygen (μs)"] <= 10 ** keypair[1])
        & (df["Sign (μs)"] >= 10 ** sign[0])
        & (df["Sign (μs)"] <= 10 ** sign[1])
        & (df["Verify (μs)"] >= 10 ** verify[0])
        & (df["Verify (μs)"] <= 10 ** verify[1])
    )
    if search:
        mask &= df["Algorithm"].str.contains(search, case=False, na=False, regex=False)

    return df.loc[mask, "Algorithm"].unique().tolist()


@callback(
    [
        Output("content-overview", "children"),
        Output("website-title", "children", allow_duplicate=True),
    ],
    [
        Input("selected-algs", "data"),
        Input("url", "pathname"),
    ],
    State("dataset-selector", "value"),
    State("clicked-algs", "data"),
    prevent_initial_call="initial_duplicate",
)
def update_shown_charts(algs, url, selected_dataset, clicked_algs):
    if url != "/sig-charts/":
        return [], no_update

    if algs is None:
        return no_update

    dataset = selected_dataset or DEFAULT_DATASET
    n_algs_total = len(_CHART_DATA[dataset])
    charts = [generate_radar_chart(alg_name, dataset, clicked_algs) for alg_name in algs]

    return charts, f"PQC Digital Signatures ({len(algs)} / {n_algs_total})"


clientside_callback(
    """
    function(radar_clicks, clicked_algs, radar_ids) {
        const ctx = window.dash_clientside.callback_context;
        if (!ctx.triggered || ctx.triggered.length === 0 || !ctx.triggered_id) {
            return window.dash_clientside.no_update;
        }
        if (ctx.triggered[0].value === 0) return window.dash_clientside.no_update;
        const noUpdate = window.dash_clientside.no_update;
        const alg = ctx.triggered_id.index.slice('radar_'.length);
        const is_selected = Boolean(clicked_algs && clicked_algs[alg]);
        const n_selected = clicked_algs ? Object.values(clicked_algs).filter(Boolean).length : 0;

        if (n_selected >= 5 && !is_selected) return [noUpdate, noUpdate];

        const new_clicked = Object.assign({}, clicked_algs || {});
        new_clicked[alg] = !is_selected;

        const new_classnames = radar_ids.map(function(rid) {
            return rid.index === ('radar_' + alg)
                ? (!is_selected ? 'radar-card radar-card--selected' : 'radar-card')
                : noUpdate;
        });
        return [new_clicked, new_classnames];
    }
    """,
    [
        Output("clicked-algs", "data", allow_duplicate=True),
        Output({"type": "radar-clickable", "index": ALL}, "className", allow_duplicate=True),
    ],
    Input({"type": "radar-clickable", "index": ALL}, "n_clicks"),
    [
        State("clicked-algs", "data"),
        State({"type": "radar-clickable", "index": ALL}, "id"),
    ],
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(dataset, clicked_algs, all_dataset_algs) {
        if (!clicked_algs || !all_dataset_algs) return window.dash_clientside.no_update;
        const available = new Set(all_dataset_algs[dataset] || []);
        let changed = false;
        const cleaned = {};
        for (const [alg, v] of Object.entries(clicked_algs)) {
            if (available.has(alg)) {
                cleaned[alg] = v;
            } else {
                changed = true;
            }
        }
        return changed ? cleaned : window.dash_clientside.no_update;
    }
    """,
    Output("clicked-algs", "data", allow_duplicate=True),
    Input("dataset-selector", "value"),
    [State("clicked-algs", "data"), State("all-dataset-algs", "data")],
    prevent_initial_call=True,
)

clientside_callback(
    """
    function(clicked, radar_ids) {
        if (!clicked) return [
            window.dash_clientside.no_update,
            window.dash_clientside.no_update,
            radar_ids.map(() => 'radar-card')
        ];
        const n_clicked = Object.values(clicked).filter(Boolean).length;
        const max_reached = n_clicked >= 5;
        const classnames = radar_ids.map(function(rid) {
            const alg = rid.index.slice('radar_'.length);
            if (clicked[alg]) return 'radar-card radar-card--selected';
            if (max_reached) return 'radar-card radar-card--disabled';
            return 'radar-card';
        });
        return ['Compare (' + n_clicked + ')', {value: n_clicked}, classnames];
    }
    """,
    [
        Output("compare-button", "children"),
        Output("n-clicked-algs", "data"),
        Output({"type": "radar-clickable", "index": ALL}, "className"),
    ],
    Input("clicked-algs", "data"),
    State({"type": "radar-clickable", "index": ALL}, "id"),
)
