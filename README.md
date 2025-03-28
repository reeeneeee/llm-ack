# LLM acknowledgments

(currently only for Mac OS and Anthropic)

Taking their inspiration from the practice of Indigenous land acknowledgements, LLM acknowledgments automatically request acknowledgment of the morally compromised provenance of the training data behind most popular LLMs [1](https://www.theverge.com/2024/8/20/24224450/anthropic-copyright-lawsuit-pirated-books-ai) [2](https://www.wired.com/story/new-documents-unredacted-meta-copyright-ai-lawsuit/) [3](https://news.bloomberglaw.com/ip-law/google-hit-with-copyright-class-action-over-imagen-ai-model) with every HTTP request to an LLM provider.

We hope to expand to more operating systems, LLM providers, and varieties of moral complicity in the future.

Currently, there are separate scripts for intercepting cURL requests to the Anthropic API and browser requests through claude.ai.

**Step 0** 

Get an [Anthropic API key](https://docs.anthropic.com/en/docs/initial-setup) and set it as an environmental variable:

`export ANTHROPIC_API_KEY='your-api-key-here'`

**Step 1**

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed. If you have Homebrew set up you can just do `brew install uv`.

Start the http proxy with the desired script:

`uv run startproxy.py <script.py>`

**Step 2**

* To make a cURL request with a given prompt:
  
`sh sample_claude_call.sh "give me a knock knock joke"`

* To chat with Claude, navigate to [claude.ai](https://claude.ai/) and initiate a conversation.


