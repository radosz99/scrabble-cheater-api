#!/bin/sh

> demo.log
gunicorn -b 0.0.0.0:8000 cheater_app.app:app

