#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Remove previous builds
rm -rf build/ dist/ *.spec

# Install PyInstaller if not already installed
python -m pip install --upgrade pyinstaller

# Build the executable with PyInstaller
pyinstaller --onefile --name mediagui mediagui/gui.py

# Move the executable to the dist directory
mv dist/mediagui dist/mediagui-executable

echo "Executable created successfully in the dist/mediagui-executable directory."