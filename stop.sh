#!/bin/bash

# Script untuk stop semua server

echo "🛑 Stopping SSB Academy Application..."

# Kill by PID files
if [ -f /tmp/ssb_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/ssb_backend.pid)
    kill $BACKEND_PID 2>/dev/null && echo "   ✅ Backend stopped (PID: $BACKEND_PID)"
    rm /tmp/ssb_backend.pid
fi

if [ -f /tmp/ssb_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/ssb_frontend.pid)
    kill $FRONTEND_PID 2>/dev/null && echo "   ✅ Frontend stopped (PID: $FRONTEND_PID)"
    rm /tmp/ssb_frontend.pid
fi

# Kill by process name (fallback)
pkill -f "python.*manage.py runserver" 2>/dev/null && echo "   ✅ Django processes stopped"
pkill -f "python.*http.server.*3000" 2>/dev/null && echo "   ✅ HTTP server processes stopped"

echo ""
echo "✅ All servers stopped!"
