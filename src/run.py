from pathlib import Path

import dash_mantine_components as dmc
import dash
from dash import Dash, _dash_renderer
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from components.appshell import create_appshell

_dash_renderer._set_react_version("18.2.0")
server = Flask(__name__)
server.wsgi_app = ProxyFix(server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
server.config["APPLICATION_ROOT"] = "/sig-charts/"

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=dmc.styles.ALL,
    url_base_pathname=server.config["APPLICATION_ROOT"],
)

app.layout = create_appshell(
    dash.page_registry.values(), server.config["APPLICATION_ROOT"]
)

if __name__ == "__main__":
    app.run_server(debug=True)
