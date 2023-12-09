#!/bin/bash
echo "Syncing Repo"
git pull
echo "Starting catbug-bot.py"
sudo nohup python3 ~/Catbug/bot/catbug-bot.py > output.log