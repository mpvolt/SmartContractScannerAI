#!/bin/bash

# Set project root
PROJECT_ROOT=$(pwd)

# Start Flask Backend
echo "🚀 Starting Flask Backend..."
if [ -d "$PROJECT_ROOT/backend" ]; then
    cd "$PROJECT_ROOT/backend"
    
    if [ ! -d "venv" ]; then
        echo "⚠️ Virtual environment not found. Creating one..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -r requirements.txt
    solc-select install 0.8.28
    solc-select use 0.8.28
    python server.py &  # Run Flask in the background
else
    echo "❌ Backend directory not found!"
    exit 1
fi

# Start React Frontend
echo "🚀 Starting React Frontend..."
if [ -d "$PROJECT_ROOT/frontend" ]; then
    cd "$PROJECT_ROOT/frontend"
    
    if [ ! -f "package.json" ]; then
        echo "⚠️ React project not found! Creating one..."
        npx create-react-app frontend
        cd frontend
        npm install
    fi

    npm start
else
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Wait for all background processes to finish
wait

echo "🌟 All processes started successfully!"