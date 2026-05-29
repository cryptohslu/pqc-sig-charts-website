import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import ALL, Input, Output, State, callback, no_update

from components.dataset import ALL_DATA, DEFAULT_DATASET, FEATURES


def soft_break_on_underscore(s: str) -> str:
    # U+200B = zero-width space (soft wrap opportunity)
    return s.replace("_", "_\u200b")


def generate_radar_chart(alg_name, df):
    data = []
    raw_data = df[df["Algorithm"] == alg_name][FEATURES].squeeze(0)
    for i, val in enumerate(raw_data):
        data.append({"feature": FEATURES[i].split("(")[0].strip(), "value": val})
    return dmc.Box(
        style={"width": "250px"},
        children=[
            dmc.Stack(
                [
                    dmc.Checkbox(
                        id={
                            "type": "checkbox-alg",
                            "index": f"checkbox-{alg_name}",
                        },
                        checked=False,
                        size="xs",
                        variant="filled",
                        label=dmc.Text(
                            soft_break_on_underscore(alg_name),
                            ta="center",
                            style={
                                "fontSize": "9pt",
                                "width": "200px",
                                "whiteSpace": "normal",
                                "overflowWrap": "anywhere",
                                "wordBreak": "break-word",
                                "lineHeight": "1.1",
                                "display": "-webkit-box",
                                "WebkitBoxOrient": "vertical",
                                "WebkitLineClamp": 2,
                                "overflow": "hidden",
                            },
                        ),
                        persistence=True,
                        persistence_type="session",
                    ),
                    dmc.RadarChart(
                        id={
                            "type": "radar-chart",
                            "index": f"radar_{alg_name}",
                        },
                        h=250,
                        w=250,
                        data=data,
                        dataKey="feature",
                        withPolarGrid=True,
                        withPolarAngleAxis=True,
                        withPolarRadiusAxis=True,
                        polarRadiusAxisProps={
                            "angle": 90,
                            "scale": "log",
                            "domain": [1, 10**5],
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
                    ),
                ],
                gap=0,
                p=0,
                align="center",
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
    [
        Output("selected-algs", "data"),
        Output("n-selected-algs", "data"),
    ],
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
    pubkey = [10 ** pubkey[0], 10 ** pubkey[1]]
    privkey = [10 ** privkey[0], 10 ** privkey[1]]
    keypair = [10 ** keypair[0], 10 ** keypair[1]]
    sign = [10 ** sign[0], 10 ** sign[1]]
    verify = [10 ** verify[0], 10 ** verify[1]]
    all_algs = df["Algorithm"].to_list()
    try:
        tmp = pd.concat([df[df["NIST Security Level"] == int(l)] for l in nist_levels])
    except ValueError:
        return {alg: False for alg in all_algs}, {"value": 0}

    if search:
        tmp = tmp[tmp["Algorithm"].str.contains(search, case=False, na=False)]
    tmp = tmp[(tmp["Pubkey (bytes)"] >= int(pubkey[0])) & (tmp["Pubkey (bytes)"] <= int(pubkey[1]))]
    tmp = tmp[(tmp["Privkey (bytes)"] >= int(privkey[0])) & (tmp["Privkey (bytes)"] <= int(privkey[1]))]
    tmp = tmp[(tmp["Signature (bytes)"] >= int(sig[0])) & (tmp["Signature (bytes)"] <= int(sig[1]))]
    tmp = tmp[(tmp["Keygen (μs)"] >= keypair[0]) & (tmp["Keygen (μs)"] <= keypair[1])]
    tmp = tmp[(tmp["Sign (μs)"] >= sign[0]) & (tmp["Sign (μs)"] <= sign[1])]
    tmp = tmp[(tmp["Verify (μs)"] >= verify[0]) & (tmp["Verify (μs)"] <= verify[1])]

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
        Output("content-overview", "children"),
        Output("website-title", "children", allow_duplicate=True),
    ],
    [
        Input("selected-algs", "data"),
        Input("n-selected-algs", "data"),
        Input("url", "pathname"),
    ],
    State("dataset-selector", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_shown_charts(algs, n_algs, url, selected_dataset):
    if url != "/sig-charts/":
        return [], no_update

    if algs is None or n_algs is None:
        return no_update

    df = ALL_DATA[selected_dataset or DEFAULT_DATASET]
    n_algs_total = df.shape[0]
    charts = [generate_radar_chart(alg_name, df) for alg_name in algs if algs[alg_name]]

    return (
        charts,
        f"PQC Digital Signatures ({n_algs["value"]} / {n_algs_total})",
    )


@callback(
    Output("clicked-algs", "data"),
    Input({"type": "checkbox-alg", "index": ALL}, "checked"),
    [
        State({"type": "checkbox-alg", "index": ALL}, "id"),
        State("url", "pathname"),
        State("clicked-algs", "data"),
    ],
)
def update_clicked_algorithms(values, ids, url, prev_clicked):
    if url == "/sig-charts/compare/":
        return no_update

    # Preserve state of filtered-out algorithms; only update what is currently visible.
    clicked_algs = dict(prev_clicked) if prev_clicked else {}
    for i, id_ in enumerate(ids):
        alg_name = "-".join(id_["index"].split("-")[1:])
        clicked_algs[alg_name] = bool(values[i])
    return clicked_algs


@callback(
    [
        Output("compare-button", "children"),
        Output("n-clicked-algs", "data"),
    ],
    Input("clicked-algs", "data"),
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
)
def disable_checkboxes(clicked, checked, selected):
    if clicked is None or selected is None:
        return len(checked) * [False]

    if clicked["value"] < 5:
        return len(checked) * [False]

    disabled_list = len(checked) * [False]
    for i, is_checked in enumerate(checked):
        if not is_checked:
            disabled_list[i] = True

    return disabled_list
