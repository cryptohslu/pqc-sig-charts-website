from pathlib import Path
import pandas as pd
import dash_mantine_components as dmc
from dash import Output, Input, dcc, page_container, State, callback

from components.header import create_header
from components.drawer import create_drawer


def create_appshell(data, url_base_pathname):
    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="dark",
        children=[
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            dmc.NotificationProvider(),
            dmc.AppShell(
                [
                    create_header(data, url_base_pathname),
                    create_drawer(data),
                    dmc.AppShellMain(children=page_container),
                ],
                header={"height": 70},
                padding="xl",
            ),
        ],
    )
