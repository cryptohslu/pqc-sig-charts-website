# pqc-sig-charts-website

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18241109.svg)](https://doi.org/10.5281/zenodo.18241109)
[![Deploy webapp](https://github.com/cryptohslu/pqc-sig-charts-website/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/cryptohslu/pqc-sig-charts-website/actions/workflows/deploy.yml)

[pqc-sig-charts.webm](https://github.com/user-attachments/assets/d51f36d6-32a4-4914-a678-ef8f34146057)

Source code of the Plotly/Dash visualization website for PQC signature algorithms.

The rawdata for the visualizations was obtained running the code available in [cryptohslu/pqc-sig-bench-c](https://github.com/cryptohslu/pqc-sig-bench-c).
The compressed Pandas dataframes from [`data`](data) were generated using the script [`generate_dataset.py`](https://github.com/cryptohslu/pqc-sig-bench-c/blob/main/scripts/generate_dataset.py).

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
@software{Mendez_Veiga_PQC_Digital_Signatures,
    author = {Mendez Veiga, Iyan},
    doi = {10.5281/zenodo.18241109},
    month = jan,
    title = {{PQC Digital Signatures Visualization}},
    url = {https://github.com/cryptohslu/pqc-sig-charts-website},
    version = {2026.01.14},
    year = {2026}
}
```

### APA

```
Mendez Veiga, I. (2026). PQC Digital Signatures Visualization (Version 2026.01.14) [Computer software]. https://doi.org/10.5281/zenodo.18241109
```
