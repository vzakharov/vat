# VAT (VSCode Agent Toolbox)

A meta-framework that empowers VSCode AI agents with command-line tools to extend their capabilities far beyond code assistance.

## Background & Overview

VAT was inspired by the transformative potential of VSCode AI agents. These agents can interact with command-line tools, essentially allowing them to do anything a human can do in a terminal - with user confirmation for safety. By providing specialized tools, VAT turns your VSCode AI into a versatile assistant capable of complex tasks.

Web search and content extraction are just the beginning. The pattern established here can be expanded to virtually any command-line capability - data processing, API interactions, media handling, and more. This creates a foundation for extending AI agent abilities without waiting for official feature releases.

## How It Works

1. Open the `base.md` prompt in your VSCode AI agent workspace (sets core behaviors)
2. Add a specific prompt file like `deep_researcher.md` (defines specialized capabilities)
3. Ask a question or give a command related to that capability

The magic happens when these two prompts combine - the agent understands both what tools are available and how to use them effectively for your specific task.

For example, with `deep_researcher.md` loaded, you might simply ask "quantum computing applications" - and the agent will:
- Search the web
- Extract and process relevant content
- Synthesize a comprehensive research report
- All while handling the command-line complexity for you

## Current Tools

- **Web Search**: Command-line interface to Exa API
- **Content Extraction**: Extract meaningful text from web pages

But the framework isn't limited to these - it's designed to be extended with any tools you can run from the command line.

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

The true potential of VAT comes from creating new tools. Any command-line program can become an extension of your AI agent's capabilities. Some ideas:
- Data analysis tools
- Image processing utilities
- API wrappers for various services
- Local database interactions

Simply create a new tool in the `tools/` directory and document its usage in your prompt files.

## Security Note

Tools run with the same permissions as your VSCode instance. The agent will ask for confirmation before running commands.