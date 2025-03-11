#!/bin/bash

while true; do
  lt --port ${2:-1218} --subdomain zeio-nara-${1:-triangle} --print-requests
done
