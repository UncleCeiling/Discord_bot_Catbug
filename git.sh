#!/bin/bash
cd /home/minipi/Catbug
git add *
git stage --all
git commit -a -m "Auto-commit"
git push
git fetch
git pull --rebase
