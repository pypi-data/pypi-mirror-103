#!/bin/bash
set -e

# Start app
source /venv/bin/activate
gunicorn main:app -w3 -b 0.0.0.0:8000 &
sleep 1

# Restart and instrument app
echo "y" | python lsi.py 
sleep 1 
curl -sf localhost:8000 && echo "Success!" || echo "Failure"

# Kill all python jobs
ps aux | grep python | awk '{print $2}' | xargs kill
