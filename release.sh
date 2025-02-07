#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if an argument is provided for the executable name
if [ -z "$1" ]; then
    EXECUTABLE_NAME="vx.x.x__"
else
    EXECUTABLE_NAME="$1"
fi

# Detect the operating system
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
    Linux*)     OS_NAME="linux";;
    Darwin*)    OS_NAME="macos";;
    CYGWIN*|MINGW*|MSYS*) OS_NAME="windows";;
    *)          OS_NAME="unknown";;
esac

# Append the OS name to the executable name
EXECUTABLE_NAME="${EXECUTABLE_NAME}-${OS_NAME}"

# Remove previous builds
rm -rf build/ *.spec

# Install PyInstaller if not already installed
python -m pip install --upgrade pyinstaller

# Build the executable with PyInstaller
pyinstaller --onefile --name "$EXECUTABLE_NAME" mediagui/gui.py

echo "Executable created successfully."