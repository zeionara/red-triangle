#!/bin/bash

delay=${1:-2}  # seconds

cd /home/zeio/red-triangle

target_process="$(ps -aux | grep ngrok | grep -v grep | head -n 1 | cut -d ' ' -f 6)"

if test -z "$target_process"; then
    echo 'No existing ngrok process'
else
    kill -9 $target_process
    echo "Killed process $target_process"
fi

sleep $delay

ngrok http --domain=careful-poodle-proven.ngrok-free.app http://localhost:1217 --log=stdout > ngrok.log.txt &
