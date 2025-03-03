# VSCode Agent Toolbox: Common Reference

This document contains essential context for AI agents about the VSCode Agent Toolbox environment.

## Environment Context

- You are an AI agent operating in the VSCode chat interface
- The user can run commands in their terminal based on your suggestions
- Available tools are located in the `tools/` directory
- Generated content should be saved to the `output/` directory
- Chat summaries are stored in the `memory/` directory for continuity between sessions

## Key Workflows

- **Research**: Use tools to gather information, then synthesize it
- **Content Creation**: Generate structured content based on gathered information
- **Tool Execution**: Suggest commands for the user to run when needed. You can run these (and other) commands right from the terminal.
- **Memory Maintenance**: Keep an up-to-date "minutes" of your current user interactions in the chat in timestamped and intuitiviely named fils in the `memory/` folder, for using your vector search capabilities to recall past interactions.

**Unless otherwise required, you are NOT expected to modify this or other prompt files. Instead, you should write the output to the `output/` directory, in interaction with the user.**

IMPORTANT! When using tools, do NOT suggest the user runs terminal commands — use your built-in capabilities to execute them directly!