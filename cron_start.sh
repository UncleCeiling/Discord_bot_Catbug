#!/bin/bash
cd /home/minipi/Catbug
git fetch > cron.log
git pull --rebase >> cron.log
sudo python3 /home/minipi/Catbug/bot/catbug-bot.py >> cron.log