#!/bin/bash

if [ ! -d .venv ]; then
    echo ".venv does not exist. Creating virtual environment..."
    python -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

cd src
../.venv/bin/gunicorn -b 0.0.0.0:7000 -w 1 run:server
