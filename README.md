# LLM acknowledgments

Taking their inspiration from the practice of Indigenous land acknowledgements, LLM acknowledgments automatically request acknowledgment of the morally compromised provenance of the training data behind most popular LLMs [1](https://www.theverge.com/2024/8/20/24224450/anthropic-copyright-lawsuit-pirated-books-ai) [2](https://www.wired.com/story/new-documents-unredacted-meta-copyright-ai-lawsuit/) [3](https://news.bloomberglaw.com/ip-law/google-hit-with-copyright-class-action-over-imagen-ai-model) with every HTTP request to an LLM provider.

We hope to expand to more LLM providers and varieties of moral complicity in the future.

**Step 0** 

Git clone this repo: `git clone https://github.com/reeeneeee/llm-ack.git`

Also, make sure you have [`uv`](https://github.com/astral-sh/uv) installed (if you have homebrew set up you can just do `brew install uv`)

**Step 1**

Start the http proxy: `uv run startproxy.py`

**Step 2**

* To make a cURL request with a given prompt:

  **Anthropic** `sh anthropic_request.sh "tell me a joke"` (optionally set `-m model_name`, see full list [here](https://docs.anthropic.com/en/docs/about-claude/models/all-models))

  **OpenAI** `sh openai_request.sh "tell me a joke"` (optionally set `-m model_name`, see full list [here](https://platform.openai.com/docs/models))

  _Note: make sure you have the relevant API key set as an environmental variable._

* To use a web interface:

  **Anthropic** Navigate to <a href="https://claude.ai/" target="_blank">claude.ai</a> and initiate a conversation.

  **OpenAI** Navigate to <a href="https://chatgpt.com/" target="_blank">chatgpt.com</a> and initiate a conversation.



