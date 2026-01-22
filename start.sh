#!/bin/bash

# Script untuk menjalankan Frontend dan Backend secara bersamaan

echo "🚀 Starting SSB Academy Application..."
echo ""

# Warna untuk output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kill existing processes
pkill -f "python.*manage.py runserver" 2>/dev/null
pkill -f "python.*http.server" 2>/dev/null

# Start Backend (Django)
echo -e "${BLUE}📦 Starting Backend (Django)...${NC}"
cd ssb
python3 manage.py runserver > /tmp/django_backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Backend URL: http://localhost:8000"
echo "   API Docs: http://localhost:8000/swagger/"
echo ""

# Wait for backend to start
sleep 3

# Start Frontend (Simple HTTP Server)
echo -e "${BLUE}🌐 Starting Frontend (HTTP Server)...${NC}"
cd ../frontend
python3 -m http.server 3000 > /tmp/frontend_server.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Frontend URL: http://localhost:3000"
echo ""

echo -e "${GREEN}✅ Application is running!${NC}"
echo ""
echo "📖 Quick Start:"
echo "   1. Open browser: http://localhost:3000"
echo "   2. Login with: admin / admin"
echo "   3. API Documentation: http://localhost:8000/swagger/"
echo ""
echo "🛑 To stop servers:"
echo "   ./stop.sh"
echo "   or manually:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Save PIDs to file for stop script
echo "$BACKEND_PID" > /tmp/ssb_backend.pid
echo "$FRONTEND_PID" > /tmp/ssb_frontend.pid

# Keep script running
echo "Press Ctrl+C to stop all servers..."
wait
