#!/bin/bash

curl \
    -H 'Content-Type: application/json' \
    -d '{"request": {"original_utterance": "foo"}, "session": {"id": 17}, "version": "1.0"}' \
    'https://careful-poodle-proven.ngrok-free.app'
