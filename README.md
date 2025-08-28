# pqc-sig-charts-website

[![DOI](https://zenodo.org/badge/926834459.svg)](https://doi.org/10.5281/zenodo.16981056)
[![Deploy webapp](https://github.com/cryptohslu/pqc-sig-charts-website/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/cryptohslu/pqc-sig-charts-website/actions/workflows/deploy.yml)

![](webapp.png)

Source code of the Plotly/Dash visualization website for PQC signature algorithms.

## Quick start

```console
$ git clone https://github.com/cryptohslu/pqc-sig-charts-website.git
$ cd pqc-sig-charts-website
$ ./run.sh
```

## Systemd units

- `pqc-sig-charts.service`: Unit that starts the Gunicorn server running the webapp
- `pqc-sig-charts-restart.service`: Auxiliary unit to restart the main service
- `pqc-sig-charts-restart.timer`: Timer that waits 30 seconds to trigger the auxiliary restart unit
- `pqc-sig-charts-debounce.path`: Unit that monitors the webapp directory for changes
- `pqc-sig-charts-debounce.service`: Unit that resets the restart timer back to 30 seconds

To enable them, copy both files to `/etc/systemd/system/` and run

```console
# systemctl enable --now pqc-sig-charts.service
# systemctl enable --now pqc-sig-charts-debounce.path
```

## Citation

If this visualization was useful to you in your research or project, please cite us.

### BibTeX

```bibtex
@software{Mendez_Veiga_PQC_Digital_Signatures_2025,
    author = {Mendez Veiga, Iyan},
    doi = {10.5281/zenodo.16981057},
    month = aug,
    title = {{PQC Digital Signatures Visualization}},
    url = {https://github.com/cryptohslu/pqc-sig-charts-website},
    version = {2025.08.28},
    year = {2025}
}
```

### APA

```
Mendez Veiga, I. (2025). PQC Digital Signatures Visualization (Version 2025.08.28) [Computer software]. https://doi.org/10.5281/zenodo.16981057
```
