#!/bin/bash

if [ ! -d venv ]; then
    echo "venv does not exist. Creating virtual environment..."
    python -m venv venv
fi

venv/bin/gunicorn -b 0.0.0.0:7000 -w 1 src.sigs:server
