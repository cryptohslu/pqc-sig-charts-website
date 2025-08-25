# pqc-sig-charts-website

![](webapp.png)

Source code of the Plotly/Dash visualization website for PQC signature algorithms.

## Quick start

```console
git clone https://github.com/cryptohslu/pqc-sig-charts-website.git
cd pqc-sig-charts-website
./run.sh
```

## Systemd units

- `pqc-sig-charts.service`: Unit that will start (and keep restarting if it failed) the Gunicorn server running the app
- `pqc-sig-charts-restart.path`: Monitor the directory with the webapp for changes
- `pqc-sig-charts-restart.service`: Triggers a one-time restart of the webapp service

To enable them, copy both files to `/etc/systemd/system/` and run

```console
systemctl enable --now pqc-sig-charts.service
systemctl enable --now pqc-sig-charts-restart.path
```
