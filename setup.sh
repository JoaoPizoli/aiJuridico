#!/bin/bash
poetry lock
poetry install
poetry show --tree >> poetry.tree
streamlit run ./src/gui/app.py 