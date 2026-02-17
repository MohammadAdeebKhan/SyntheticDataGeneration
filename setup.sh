#!/bin/bash

echo ""
echo "========================================"
echo "Data Generation Platform Setup"
echo "========================================"
echo ""

if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source env/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created. Please edit it with your credentials."
else
    echo ".env file already exists."
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Run: streamlit run streamlit_app.py"
echo "3. Open: http://localhost:8501"
echo ""
