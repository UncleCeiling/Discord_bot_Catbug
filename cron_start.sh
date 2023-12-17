#!/bin/bash
cd /home/minipi/Catbug
git fetch
git pull --rebase
python3 bot/catbug-bot.py >> cron.log