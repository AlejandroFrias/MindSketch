#!/bin/bash

echo "Creating Sublime Text 3 plugin"

# Usage: ./mindsketch mindsketch_file_name [output_plugin_name]
source venv/bin/activate
python ./source/code/create_plugin.py $1 ${2:-mind_sketch.py}