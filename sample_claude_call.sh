#!/bin/sh
curl -s https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data \
'{
    "model": "claude-3-5-haiku-20241022",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "$1"}  
    ]
}' | jq -r '.content[0].text' | tee /dev/tty | say --rate 225
