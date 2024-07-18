#!/bin/bash

# Navigate to your script's directory
cd /Users/syed44/telebot/atmocean/

# Specify the full path to the Python interpreter
# python_path="/Users/syed44/miniconda3/bin/python"
python_path="/Users/syed44/miniconda3/envs/radar/bin/python"

# Run your Python script using the specified Python interpreter
$python_path post_jobs.py
# $python_path bot_status.py

