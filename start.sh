#!/bin/bash
echo "Syncing Repo"
git fetch
echo "Starting catbug-bot.py"
sudo nohup python3 ~/Catbug/bot/catbug-bot.py > output.log