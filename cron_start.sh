#!/bin/bash
cd /home/minipi/Catbug
git fetch
git pull --rebase
sudo python3 /home/minipi/Catbug/bot/catbug-bot.py >> cron.log