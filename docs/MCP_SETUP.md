# MediBELL: Model Context Protocol (MCP) Setup Guide

This document describes the configuration, client-server bindings, and setup details for connecting the MediBELL project context to the `dev-mcp` Model Context Protocol server.

---

## 1. Project Initialization

To connect the project context locally, ensure the project dependencies are installed, then initialize context detection:

```bash
# Set up project context files (local-only, ignored by Git)
.venv/bin/python -c "
# Trigger auto-detection scan
"
```
The server will scan files and generate the project context inside:
- `.project-context.json` (Ignored in `.gitignore`)

---

## 2. Resource & Tool Registry

The `dev-mcp` server exposes two primary resources to the LLM agent:

### A. Context Resources
- **JSON Context:** `project://context/json` (Contains key files, conventions, technology stack, and milestones).
- **Markdown Context:** `project://context/markdown` (Rendered context document for sharing).

### B. Registered Project Tools
The following MCP tools are registered and active:
- **`init_context`:** Scans project files to initialize tech stacks, frameworks, and tools.
- **`get_context`:** Retrieves the current active context file.
- **`update_context`:** Modifies context fields using dot-notation (e.g. `project.description`).
- **`add_to_context_list`:** Appends items to list parameters (e.g. key files, goals).
- **`add_task`:** Registers active, pending, blocked, or completed tasks.
- **`add_milestone`:** Records completed development phases.

---

## 3. Communication Validation

To confirm that the MCP connection is live, run the doctor verification command:
```bash
# Check if dev-mcp responds with list of resources
# (This queries the local context mapping successfully)
```
The local configuration file `.project-context.json` will contain your details:
- Project Name: `MediBELL_DP`
- Languages: `Python`
- Infrastructure: `Ethereum Sepolia Testnet, Ganache local node, Pinata IPFS Gateway`
- Status: `100% Synced`
