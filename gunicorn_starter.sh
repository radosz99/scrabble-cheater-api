#!/bin/sh

kill $(lsof -t -i:8000) 
gunicorn -b 0.0.0.0:8000 cheater_app.app:app --daemon

