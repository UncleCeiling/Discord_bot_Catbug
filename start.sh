#!/bin/bash
cd ~/Catbug
git fetch
git pull --rebase
sudo nohup python3 ~/Catbug/bot/catbug-bot.py
