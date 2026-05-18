#!/bin/sh

echo "Running update check..."
python3 update.py

echo "Starting bot..."
python3 bot.py
