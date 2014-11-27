#!/bin/bash

echo "Bootstrapping MindSketch"

echo "Installing virtualenv"
pip install virtualenv

echo "Creating Python Virtual Environment venv"
virtualenv venv

# Activate virtual environment and install necessary packages
echo "Installing Packages"
source venv/bin/activate
pip install pypeg2
pip install collections
pip install unittest
pip install nose