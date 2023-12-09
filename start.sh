#!/bin/bash
cd ~/Catbug
git fetch
git pull --rebase
sudo python3 ~/Catbug/bot/catbug-bot.py