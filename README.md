## llm-agent-playground

This repository is a playground for experimenting with **multi‑agent LLM research pipelines**.  
It uses `openai-agents`, `google-adk`, and MCP (Model Context Protocol) servers to automate the following **research workflow**:

- **0. Guardrail**: Decide whether the user’s request actually requires research work
- **1. Plan**: Generate a web search plan (search queries)
- **2. Research**: Run MCP‑based web search and produce a research report
- **3. Summarize**: Summarize the research results into a Markdown report (Korean by default in the example)

The entry point `orchestration_agent.py` runs an orchestrator agent that coordinates all of these steps.

---

## Features

- **Orchestration agent**
  - `orchestration(topic: str)` in `orchestration_agent.py`
  - Executes Guardrail / Planner / Research / Summarize agents as a single research workflow

- **OpenAI‑based agents (`openai_agents/`)**
  - **`guardrail_agent.py`**
    - Classifies whether the user input requires research (`is_research_work` flag)
  - **`planner_agent.py`**
    - Creates a search plan based on a Pydantic model (`WebSearchPlan`)
  - **`research_agent.py`**
    - Uses an MCP server (`serper-mcp-server`) to perform web search
    - Returns a `ResearchReport` (short summary + full report)
  - **`summarize_agent.py`**
    - Uses a filesystem MCP server to write a Markdown report into the `report` directory
    - Responds with **only the file path** of the created report

- **Google ADK examples (`google_adk/`)**
  - Example implementations of Planner / Research / Summarize with the Google ADK style

- **Shared configuration (`configuration/configuration.py`)**
  - Loads environment variables from `.env`
  - Sets up basic logging
  - Configures observability/tracing with `opik`

---

## Installation

This project requires **Python 3.13+**.

```bash
git clone <your-repo-url>
cd llm-agent-playground

uv sync
```

Key dependencies are declared in `pyproject.toml`, including:

- `openai-agents`
- `google-adk`
- `mcp[cli]`
- `opik`
- `python-dotenv`
- `httpx`, `litellm`, etc.

---

## Environment variables

Create a `.env` file in the project root and set the following values:

```env
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
OPIK_API_KEY=...
SERPER_API_KEY=...
```

They are used in the following places:

- **`OPENAI_API_KEY`**: Calling OpenAI models (`gpt-5-mini`, `gpt-5-nano`, `gpt-4o-mini`, etc.)
- **`GOOGLE_API_KEY`**: Calling Gemini models via `google-adk` (e.g., `gemini-2.5-flash` in the `google_adk` examples)
- **`OPIK_API_KEY`**: Tracing and logging via `opik`
- **`SERPER_API_KEY`**: Web search via `serper-mcp-server`

---

## Usage

### 1. Run the orchestration agent

`orchestration_agent.py` is an example script that runs the full research workflow.

```bash
python orchestration_agent.py
```

By default, it runs with the following topic:

```python
asyncio.run(orchestration("What is my name?"))
```

To customize the topic, you can either edit the call at the bottom of `orchestration_agent.py`, or create your own entry script, for example:

```python
from orchestration_agent import orchestration
from configuration.configuration import configure_all
import asyncio

if __name__ == "__main__":
    configure_all()
    asyncio.run(orchestration("Your custom research topic"))
```

### 2. Run individual agents

- **Planner only**

```bash
python openai_agents/planner_agent.py
```

- **Research only**

```bash
python openai_agents/research_agent.py
```

- **Summarization only**

```bash
python openai_agents/summarize_agent.py
```

Each script contains a sample `if __name__ == "__main__":` block demonstrating its usage.

---

## MCP servers

This project relies on MCP (Model Context Protocol)‑based tools.

- **Web research MCP server**
  - Command: `uvx serper-mcp-server`
  - Used in: `openai_agents/research_agent.py` (`create_research_mcp_server`)
  - Required environment variable: `SERPER_API_KEY`

- **Filesystem MCP server**
  - Command: `npx -y @modelcontextprotocol/server-filesystem <project_root>`
  - Used in: `openai_agents/summarize_agent.py` (`create_summarize_mcp_server`)
  - Role: Create and store Markdown reports under the `report` directory

Make sure `uvx` and `npx` are available on your `PATH` (i.e., `uv` and Node.js are installed and configured).

---

## Project structure

```text
llm-agent-playground/
  orchestration_agent.py      # Orchestrates the full research workflow
  configuration/
    configuration.py          # Logging, .env loading, Opik configuration
  openai_agents/
    guardrail_agent.py        # Decides whether research is needed
    planner_agent.py          # Generates web search plans
    research_agent.py         # MCP web research & report generation
    summarize_agent.py        # Creates Markdown report (filesystem MCP)
    evaluator_agent.py        # (future) result evaluation agent
  google_adk/
    planner_agent.py          # Planner example in Google ADK style
    research_agent.py         # Research example in Google ADK style
    summarize_agent.py        # Summarizer example in Google ADK style
    report/
      title.md                # Sample/title report
```

---

## Notes for development

- This repository is primarily intended as an **example project** to explore:
  - Multi‑agent orchestration patterns, and
  - MCP‑based tool calling.
- For production use, you will likely want to:
  - Add more robust error handling
  - Monitor and control token usage / cost
  - Implement additional guardrails and monitoring
  - Extend and harden the report schema and storage
  and integrate these agents into your broader application architecture.
