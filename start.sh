#!/bin/sh
echo "> Updating from Github";
git pull;
echo "> Composing container";
docker compose up --build -d;
EXIT_CODE=$(docker wait catbug);
echo "Exited with $EXIT_CODE";