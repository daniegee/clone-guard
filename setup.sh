#!/bin/bash

# Initialise git submodules
echo "Initialising git submodules..."
git submodule update --init --recursive

# Install required Python packages
echo "Installing required Python packages..."
pip install -r requirements.txt
