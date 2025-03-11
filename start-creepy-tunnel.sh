#!/bin/bash

while true; do
  lt --port ${2:-1219} --subdomain zeio-nara-${1:-creepy} --print-requests
done
