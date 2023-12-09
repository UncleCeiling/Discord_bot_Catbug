#!/bin/bash
cd ~/Catbug
git pull --rebase
sudo python3 ~/Catbug/bot/catbug-bot.py > output.log