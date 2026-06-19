# MediBELL: Model Context Protocol (MCP) Architecture

This document defines the architectural boundaries and information flow between the IDE, the LLM agent, and the `dev-mcp` project context server.

---

## 1. Information Flow Diagram

```
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│  LLM Agent   │ ─────────► │  dev-mcp     │ ─────────► │  .project-   │
│  (AI Coder)  │ ◄───────── │  MCP Server  │ ◄───────── │ context.json │
└──────────────┘            └──────────────┘            └──────────────┘
       │
       ▼
┌──────────────┐
│ Project IDE  │
│  Workspace   │
└──────────────┘
```

1. **Context Initialization:** The LLM agent initializes the context via the `init_context` tool, prompting `dev-mcp` to scan the workspace directory.
2. **Persistence:** The `dev-mcp` server writes project state updates (such as active tasks, conventions, stack changes) directly to `.project-context.json`.
3. **Retrieval:** When the LLM agent needs to analyze project guidelines or milestones, it reads the context via `project://context/json`, maintaining state alignment across chat turns.

---

## 2. Context Schema Mapping

The local metadata schema tracks the following properties:

* **`project`:** Contains naming conventions, version bounds, description, and timestamps.
* **`tech_stack`:** Groups languages, tools, frameworks, and infrastructure dependencies.
* **`architecture`:** Houses architectural overview summaries, directories, and required coding patterns.
* **`conventions`:** Defines PEP8 style guides, git branch workflows, and unit testing strategies.
* **`key_files`:** Tracks files critical for integration and deployment (e.g. smart contracts, API controllers, uploader files).
* **`milestones`:** Logs completed development phases.
