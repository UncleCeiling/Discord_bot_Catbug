#!/bin/bash
cd /home/minipi/Catbug
git fetch
git pull --rebase
sudo python3 bot/catbug-bot.py