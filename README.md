# VAT (VSCode Agent Toolbox)

A meta-framework that extends VSCode AI agents' capabilities through command-line tools.

## Background & Overview

VAT was inspired by the transformative potential of VSCode AI agents. These agents can interact with command-line tools, essentially allowing them to do anything a human can do in a terminal — with user confirmation for safety. By providing specialized tools, you're extending your AI assistant's capabilities far beyond code assistance.

For example, take web search and content extraction. OpenAI has recently created their Deep Research feature, which is mindblowing on its own — but with the VAT approach, you can replicate it by just combining a few command-line tools and a well-crafted prompt. The AI agent then handles all the complexity: searching, extracting content, evaluating the results, searching again with refined queries, until it has gathered enough meaningful information to synthesize a comprehensive response.

This pattern can expand to virtually any command-line capability — data processing, API interactions, media handling, and more. It creates a foundation for extending AI agent abilities without waiting for official feature releases.

## How It Works

1. Open `base.md` in your VSCode AI agent workspace and lock it in the working set (click the lock icon)
2. Open a specific prompt like `deep_researcher.md` — it's automatically added to your working set
3. Ask a question or give a command related to that capability

The magic happens when these two prompts combine — the agent understands both what tools are available and how to use them effectively for your specific task.

For example, with `deep_researcher.md` loaded, you might ask "quantum computing applications". The agent will:
- Search the web for initial sources
- Extract and analyze the content
- Identify knowledge gaps and search again with refined queries
- Repeat this process until it has gathered comprehensive information
- Synthesize everything into a well-structured report
- All while handling the command-line complexity for you

## Current Tools

- **Web Search**: Command-line interface to Exa API
- **Content Extraction**: Extract meaningful text from web pages

But that's just the start — the framework is designed to work with any command-line tool you can create.

---

## Installation

1. Clone and enter:
```bash
git clone https://github.com/yourusername/vat.git
cd vat
```

2. Run setup:
```bash
./setup.sh
```

3. Configure:
```
# In .env file
EXA_API_KEY=your_api_key_here
DEFAULT_SEARCH_LIMIT=10
```

## Project Structure

```
.
├── tools/            # Command-line tools for agents to use
├── prompts/          # Agent behavior definitions
│   ├── base.md       # Core capabilities and environment
│   └── deep_researcher.md  # Research specialist profile
├── src/              # Underlying functionality
├── output/           # Generated content
└── memory/           # Session histories
```

## Tool Reference

### Web Search
```bash
python tools/exa.py --query "search query" --limit 10
```

### Content Extraction
```bash
python tools/soup.py --url "https://example.com" --selector "optional_css_selector"
```

## Dependencies

- Python 3.8+
- VSCode with AI capabilities (GitHub Copilot Chat or similar)
- Python packages: beautifulsoup4, requests, python-dotenv, inflect

## Development

Install in development mode:
```bash
pip install -e .
```

## Extending VAT

The true potential of VAT comes from creating new tools and prompts. Any command-line program can become an extension of your AI agent's capabilities. Some ideas:
- Data analysis tools
- Image processing utilities
- API wrappers for various services
- Local database interactions

Simply create a new tool in the `tools/` directory and document its usage in your prompt files.

Feel free to fork the repository and submit pull requests with your own prompts and tools — let's expand the possibilities together!

## Security Note

Tools run with the same permissions as your VSCode instance. The agent will ask for confirmation before running commands.