#!/bin/sh

# To run this script, you need to set the OPENAI_API_KEY environment variable.
# You can do this by running `export OPENAI_API_KEY=<your-api-key>`.

# Example: ./openai_request.sh "Tell me a joke"
# Example: ./openai_request.sh -m gpt-4o "What is the capital of France?"


# Default model
MODEL="gpt-4o"

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

RESPONSE=$(curl -s https://api.openai.com/v1/responses \
     --header "content-type: application/json" \
     --header "Authorization: Bearer $OPENAI_API_KEY" \
     --data "{
    \"model\": \"$MODEL\",
    \"input\": \"$1\"
}" | jq -r '.output[0].content[0].text')

echo "$RESPONSE"
echo "$RESPONSE" | say --rate 225 &

unset http_proxy
unset https_proxy
