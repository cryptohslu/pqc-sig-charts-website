import dash
import secure
from dash import Dash
from flask import Flask, Response
from werkzeug.middleware.proxy_fix import ProxyFix

from components.appshell import create_appshell

server = Flask(__name__)
server.wsgi_app = ProxyFix(server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
server.config["APPLICATION_ROOT"] = "/sig-charts/"

# Custom CSP policy
csp = (
    secure.ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'", "'unsafe-inline'")
    .style_src("'self'", "'unsafe-inline'")
    .object_src("'none'")
)
secure_headers = secure.Secure(csp=csp)


@server.after_request
def set_secure_headers(response: Response):
    secure_headers.set_headers(response)
    return response


app = Dash(
    __name__,
    server=server,
    use_pages=True,
    url_base_pathname=server.config["APPLICATION_ROOT"],
)

app.layout = create_appshell(dash.page_registry.values(), server.config["APPLICATION_ROOT"])

if __name__ == "__main__":
    app.run(debug=True)
