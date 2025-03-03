# VAT (VSCode Agent Toolbox)

A toolset that extends VSCode AI agents with web research and content extraction capabilities.

## Overview

VAT provides command-line tools that enable VSCode AI agents to:
- Search the web using the Exa API
- Extract content from web pages using BeautifulSoup
- Process and structure research results

## How It Works

1. Open the base prompt (defines core behavior and tool interactions)
2. Add a specific prompt (like `deep_researcher.md`) to define the task-specific behavior
3. The AI agent then follows these prompts, using the provided tools to accomplish tasks

For example, with the deep researcher prompt loaded, you could simply ask "consciousness in AI", and the agent would:
- Use `exa.py` to perform targeted web searches
- Extract relevant content with `soup.py`
- Synthesize the findings into structured research output

## Installation

1. Clone and enter the repository:
```bash
git clone https://github.com/yourusername/vat.git
cd vat
```

2. Run setup:
```bash
./setup.sh
```

3. Configure:
- The setup creates `.env` from `.env.example`
- Add your Exa API key:
```
EXA_API_KEY=your_api_key_here
DEFAULT_SEARCH_LIMIT=10
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

## Project Structure

```
.
├── tools/            # Command-line tools
│   ├── exa.py       # Web search using Exa API
│   └── soup.py      # Web content extraction
├── prompts/         # Agent behavior definitions
├── src/             # Core functionality
├── output/          # Generated content
└── memory/          # Session histories
```

## Dependencies

- Python 3.8+
- VSCode with AI capabilities
- Exa API key
- Python packages: beautifulsoup4, requests, python-dotenv, inflect

## Development

Install in development mode:
```bash
pip install -e .
```

## Background

VAT was inspired by the combination of VSCode AI agents and OpenAI's research capabilities in ChatGPT. It aims to bring similar functionality to VSCode's AI agents through a set of command-line tools.

## Security Note

Keep your API keys secure. The `.env` file is listed in `.gitignore` by default.