#!/bin/bash

VENV_DIR=~/.venv
MAT_DIR="${VENV_DIR}/materialista"

mkdir -p "$VENV_DIR"
virtualenv -p python3 "$MAT_DIR"
source "{MAT_DIR}"/bin/activate
pip install -r requirements.txt
