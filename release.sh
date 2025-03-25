#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if an argument is provided for the executable name
if [ -z "$1" ]; then
    EXECUTABLE_NAME="mediagui"
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

# Define the version
VERSION="v1.0.0"

# Append the OS name and version to the executable name
EXECUTABLE_NAME="${EXECUTABLE_NAME}-${OS_NAME}-${VERSION}"

# Remove previous builds
rm -rf build/ dist/

# Install PyInstaller if not already installed
python -m pip install --upgrade pyinstaller

# Set the EXECUTABLE_NAME environment variable
export EXECUTABLE_NAME="$EXECUTABLE_NAME"

# Build the executable with PyInstaller
pyinstaller mediaGUI.spec

echo "Executable created successfully in the dist/$EXECUTABLE_NAME directory."

# Create zip archive
cd dist
if [ "$OS_NAME" = "windows" ]; then
    # Use zip command if available, otherwise try 7z
    if command -v zip >/dev/null 2>&1; then
        zip -r "${EXECUTABLE_NAME}.zip" "$EXECUTABLE_NAME"
    elif command -v 7z >/dev/null 2>&1; then
        7z a "${EXECUTABLE_NAME}.zip" "$EXECUTABLE_NAME"
    else
        echo "Warning: Neither zip nor 7z found. Skipping zip creation."
    fi
else
    # Use zip on Unix-like systems
    zip -r "${EXECUTABLE_NAME}.zip" "$EXECUTABLE_NAME"
fi
cd ..

echo "Build complete! Output files:"
echo "- Executable directory: dist/$EXECUTABLE_NAME"
echo "- Zip archive: dist/${EXECUTABLE_NAME}.zip"