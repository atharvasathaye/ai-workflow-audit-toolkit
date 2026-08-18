# Engineering Workflow automation Audit & MCP Toolkit

This toolkit provides engineering teams with a structured methodology and the technical infrastructure to measure the actual ROI of automation coding assistants (like new code generation tools).

It moves the conversation from "the new tool feels faster" to "the new tool saved us 25% on these specific tasks, but is net-negative on architectural refactoring unless provided with sprint context."

## Components

1. **Measurement Protocol (`docs/measurement_protocol.md`):** A rigorous framework for instrumenting 15 recurring sprint tasks and tracking baseline vs. assisted time.
2. **Mock Data & Dashboard (`data/`, `dashboard/`):** A Streamlit dashboard visualizing the audit results, highlighting time saved, rework rates, and task categories where automation struggles.
3. **GitHub Projects MCP Server (`mcp_server/`):** A Python-based Model Context Protocol (MCP) server that gives the CLI tool direct access to your live sprint backlog and tickets, eliminating the need to copy-paste context.
4. **Adoption Materials (`docs/`):** Templates for executive rollout recommendations and internal team presentations.

## Setup Instructions

### 1. The Dashboard
To view the audit results:
```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

### 2. The MCP Server
The MCP server exposes tools (`get_open_tickets`, `get_sprint_burndown`) to the CLI tool using the GitHub API. It relies on the GitHub CLI (`gh`) being authenticated.

```bash
cd mcp_server
pip install -r requirements.txt
```

To configure the CLI tool to use this MCP server, add it to your Claude configuration or run it locally according to the MCP spec.

### 3. Seeding Mock Data
If you want to test the MCP server on this repository, you can generate a mock 3-sprint backlog:
```bash
cd scripts
python seed_github_backlog.py
```
*(Requires `gh` CLI authenticated with repo permissions)*

## Why This Matters
Automation tools are only as good as the context they are given. By using MCP to connect the CLI tool directly to our project management tools, and by rigorously measuring the outcome, we can implement targeted, ROI-positive tool adoption rather than relying on hype.
