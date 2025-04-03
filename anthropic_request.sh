#!/bin/sh

# To run this script, you need to set the ANTHROPIC_API_KEY environment variable.
# You can do this by running `export ANTHROPIC_API_KEY=<your-api-key>`.

# Example: ./anthropic_request.sh "Tell me a joke"
# Example: ./anthropic_request.sh -m claude-3-5-haiku-20241022 "What is the capital of France?"


# Default model
MODEL="claude-3-5-haiku-20241022"

# Parse command line arguments
while getopts "m:" opt; do
  case $opt in
    m) MODEL="$OPTARG" ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
  esac
done

# Shift the parsed options, leaving only the message
shift $((OPTIND-1))

# Check if message is provided
if [ -z "$1" ]; then
    echo "Usage: $0 [-m model] message"
    exit 1
fi

export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080

RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
     --header "x-api-key: $ANTHROPIC_API_KEY" \
     --header "anthropic-version: 2023-06-01" \
     --header "content-type: application/json" \
     --data "{
    \"model\": \"$MODEL\",
    \"max_tokens\": 1024,
    \"messages\": [
        {\"role\": \"user\", \"content\": \"$1\"}  
    ]
}" | jq -r '.content[0].text')

echo "$RESPONSE"
echo "$RESPONSE" | say --rate 225 &

unset http_proxy
unset https_proxy
