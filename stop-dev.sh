#!/bin/bash

# SSB Academy - Stop Development Servers Script

echo "🛑 Stopping SSB Academy Development Servers..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to kill process
kill_process() {
    if [ -f "$1" ]; then
        PID=$(cat "$1")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID 2>/dev/null
            sleep 1
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                kill -9 $PID 2>/dev/null
            fi
            echo -e "${GREEN}✅ Stopped process $PID${NC}"
        else
            echo -e "${YELLOW}⚠️  Process $PID not running${NC}"
        fi
        rm "$1"
    else
        echo -e "${YELLOW}⚠️  PID file $1 not found${NC}"
    fi
}

# Stop Django
echo "Stopping Django Backend..."
kill_process /tmp/ssb-django.pid

# Stop Vue
echo "Stopping Vue Frontend..."
kill_process /tmp/ssb-vue.pid

# Kill any remaining processes on ports
echo ""
echo "Cleaning up ports..."
if lsof -ti:8000 >/dev/null 2>&1; then
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo "✅ Port 8000 freed"
fi

if lsof -ti:5173 >/dev/null 2>&1; then
    lsof -ti:5173 | xargs kill -9 2>/dev/null
    echo "✅ Port 5173 freed"
fi

# Clean up log files
if [ -f /tmp/django-ssb.log ]; then
    rm /tmp/django-ssb.log
    echo "🗑️  Cleaned Django logs"
fi

if [ -f /tmp/vue-ssb.log ]; then
    rm /tmp/vue-ssb.log
    echo "🗑️  Cleaned Vue logs"
fi

echo ""
echo -e "${GREEN}✅ All servers stopped and cleaned up!${NC}"
