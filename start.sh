#!/bin/sh
while true; do
    # Update
    echo ">> Updating from Github."
    git pull
    # Start container and wait for exit code
    echo ">> Composing container."
    # code=$(docker compose up --build)
    docker compose up --build -d
    code=$(docker wait catbug)
    echo ">> Catbug exited with $code."
    if [$code -ne 0]; then
        echo ">> Stopping."
        exit 1
    fi
    echo ">> Restarting."
    sleep 10s
done