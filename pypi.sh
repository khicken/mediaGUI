#!/bin/bash

# Make sure to update the version in setup.py before running this script

# Exit immediately if a command exits with a non-zero status
set -e

# Remove previous builds
rm -rf dist/

# Build the source and wheel distributions
python -m pip install --upgrade setuptools wheel build
python -m build

# Upload the package to PyPI
python -m pip install --upgrade twine
python -m twine upload dist/*