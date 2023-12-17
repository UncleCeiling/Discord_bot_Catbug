#!/bin/bash
cd /home/minipi/Catbug
git fetch --all
git reset --hard
git stash pop
git pull
python3 /home/minipi/Catbug/bot/catbug-bot.py