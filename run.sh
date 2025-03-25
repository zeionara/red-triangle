#!/bin/bash

# sudo MISTRAL_API_KEY="$MISTRAL_API_KEY" python -m rt serve -m 'mistral-large-latest' -c 'creepy-mistral' --concise --key $SSL_KEY_PATH --cert $SSL_CERT_PATH -p 443
python -m rt serve -m 'mistral-large-latest' -c 'creepy-mistral' --concise -p 1219
