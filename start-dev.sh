#!/bin/bash

# SSB Academy - Development Starter Script
# This script starts both Django backend and Vue frontend

echo "🚀 Starting SSB Academy Development Servers..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Kill process on port if needed
kill_port() {
    if check_port $1; then
        echo -e "${YELLOW}⚠️  Port $1 is in use. Killing process...${NC}"
        lsof -ti:$1 | xargs kill -9 2>/dev/null
        sleep 2
    fi
}

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Clean up old PIDs
rm -f /tmp/ssb-django.pid /tmp/ssb-vue.pid

# Start Django Backend
echo -e "${BLUE}📡 Starting Django Backend...${NC}"
kill_port 8000
cd "$SCRIPT_DIR/ssb"

# Check if python3 or python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

nohup $PYTHON_CMD manage.py runserver 0.0.0.0:8000 > /tmp/django-ssb.log 2>&1 &
DJANGO_PID=$!
echo "$DJANGO_PID" > /tmp/ssb-django.pid
echo "   Backend PID: $DJANGO_PID"
echo "   Backend URL: http://localhost:8000"
echo "   Swagger UI: http://localhost:8000/swagger/"
echo ""

# Wait for Django to start
echo "   Waiting for Django to start..."
sleep 4

# Check if Django is actually running
if ! check_port 8000; then
    echo -e "${YELLOW}⚠️  Django may have failed to start. Check logs: tail -f /tmp/django-ssb.log${NC}"
fi

# Start Vue Frontend
echo -e "${BLUE}🎨 Starting Vue Frontend...${NC}"
kill_port 5173
cd "$SCRIPT_DIR/frontend-ssb"

nohup npm run dev > /tmp/vue-ssb.log 2>&1 &
VUE_PID=$!
echo "$VUE_PID" > /tmp/ssb-vue.pid
echo "   Frontend PID: $VUE_PID"
echo "   Frontend URL: http://localhost:5173"
echo ""

# Wait for Vue to start
echo "   Waiting for Vue to start..."
sleep 5

# Check if Vue is running
if ! check_port 5173; then
    echo -e "${YELLOW}⚠️  Vue may have failed to start. Check logs: tail -f /tmp/vue-ssb.log${NC}"
fi

echo ""
echo -e "${GREEN}✅ All servers started!${NC}"
echo ""
echo "📝 Access Points:"
echo "   • Frontend: http://localhost:5173"
echo "   • Backend: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/swagger/"
echo ""
echo "🔐 Login Credentials:"
echo "   • Username: admin"
echo "   • Password: admin"
echo ""
echo "📊 Logs:"
echo "   • Django: tail -f /tmp/django-ssb.log"
echo "   • Vue: tail -f /tmp/vue-ssb.log"
echo ""
echo "🛑 To stop servers: ./stop-dev.sh"
echo ""
echo "💡 If servers don't start, check the logs above"
echo ""
