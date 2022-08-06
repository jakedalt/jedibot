#!/usr/bin/env bash


py -3.9 -m venv venv || exit
# ( \/ windows only \/ )
. venv/Scripts/activate
pip install -r requirements.txt
deactivate
