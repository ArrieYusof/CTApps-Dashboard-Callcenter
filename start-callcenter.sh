#!/bin/zsh
# Version: 0.1
# Last Modified: 2025-08-22
# Changes: Script to start VADS Call Center wireframe Dash app

# Activate virtual environment if exists
    # Activate conda environment
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate llms

# Install required packages if not present
pip install dash dash-bootstrap-components plotly

# Run the Dash app
python callcenter_app/app.py
