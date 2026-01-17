#!/bin/bash
# Setup Python Virtual Environment for Lottery Analyzer
# Linux/Mac bash script

echo "Creating Python virtual environment..."
python3 -m venv lottery_env

echo ""
echo "Activating virtual environment..."
source lottery_env/bin/activate

echo ""
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================"
echo "Virtual environment setup complete!"
echo "============================================"
echo ""
echo "To activate the environment in the future:"
echo "  source lottery_env/bin/activate"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "To run Jupyter notebooks:"
echo "  jupyter notebook"
echo "============================================"
