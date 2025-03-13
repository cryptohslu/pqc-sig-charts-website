import dash_mantine_components as dmc


def generate_instructions_alert():
    return dmc.Box(
        [
            dmc.Alert(
                [
                    dmc.Highlight(
                        "1. Explore the post-quantum digital signature algorithms in the overview page.",
                        ta="left",
                        highlight=["Explore", "overview"],
                        highlightStyles={
                            "backgroundImage": "linear-gradient(45deg, var(--mantine-color-cyan-5), var(--mantine-color-indigo-5))",
                            "fontWeight": 500,
                            "WebkitBackgroundClip": "text",
                            "WebkitTextFillColor": "transparent",
                        },
                    ),
                    dmc.Space(h=5),
                    dmc.Image(
                        radius="md",
                        src="/sig-charts/assets/overview.png",
                        h=315,
                        w=476,
                    ),
                    dmc.Space(h=5),
                    dmc.Highlight(
                        "2. Filter algorithms in the left panel by selecting desired key and signature lengths, and performance times.",
                        ta="left",
                        highlight=["Filter"],
                        highlightStyles={
                            "backgroundImage": "linear-gradient(45deg, var(--mantine-color-cyan-5), var(--mantine-color-indigo-5))",
                            "fontWeight": 500,
                            "WebkitBackgroundClip": "text",
                            "WebkitTextFillColor": "transparent",
                        },
                    ),
                    dmc.Highlight(
                        "3. Compare up to 5 algorithms simulatenously in the comparison page.",
                        ta="left",
                        highlight=["Compare", "comparison"],
                        highlightStyles={
                            "backgroundImage": "linear-gradient(45deg, var(--mantine-color-cyan-5), var(--mantine-color-indigo-5))",
                            "fontWeight": 500,
                            "WebkitBackgroundClip": "text",
                            "WebkitTextFillColor": "transparent",
                        },
                    ),
                    dmc.Space(h=5),
                    dmc.Image(
                        radius="md",
                        src="/sig-charts/assets/compare.png",
                        h=350,
                        w=476,
                    ),
                    dmc.Space(h=5),
                ],
                title="Welcome to PQC Sig Charts!",
                id="alert-instructions",
                color="blue",
                withCloseButton=True,
            ),
            dmc.Space(h=20),
        ]
    )
