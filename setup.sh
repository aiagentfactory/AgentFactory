#!/bin/bash

echo "Setting up Agent Factory Environment..."

# Backend Setup
echo "Installing Backend Dependencies..."
pip install -r server/requirements.txt
# Ensure pytest is installed for testing
pip install pytest httpx

# Frontend Setup
echo "Installing Frontend Dependencies..."
cd client
npm install
cd ..

echo "Setup Complete! Run './run.sh' to start the application."
