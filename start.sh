#!/bin/sh
echo "> Updating from Github";
git pull;
echo "> Composing container";
docker compose up --build -d
docker wait catbug
EXIT_CODE = $?;
echo $EXIT_CODE;