# MaybeAI Runtime Architecture

> **Status: 2026-04-20** — This documents the current active runtime. `maybe.ai` (build/frontend) is rarely updated; the runtime it depends on is actively developed.

---

## What Is the Runtime

The **MaybeAI runtime** is the engine that executes AI workflows. It is not a single service — it is a stack of three services that together provide workflow execution, tool routing, and AI agent orchestration.

| Service | Repo | Role |
|---------|------|------|
| `fastestai-api` | `fastestai-api/` | Workflow runtime + 40+ native tools + MCP routing |
| `fastestai-playground` | `fastestai-playground/` | Auth, sessions, payments, chat, user/org management |
| `omnimcp-be` | `omnimcp-be/` | MCP server discovery, tool indexing, semantic search (Qdrant) |

The **frontend** (`app-factory/apps/chat`, `app-factory/apps/clawAI`) calls `fastestai-playground` (auth) then `fastestai-api` (execution).

The **CLI** (`cli/maybeai-app` + `cli/app-cli`) also calls `fastestai-api` but skips the frontend — lower token cost, simpler for AI consumption.

---

## System Architecture

```
                              ┌─────────────────────────────────┐
                              │         Frontend                 │
                              │  app-factory/apps/chat          │
                              │  app-factory/apps/clawAI         │
                              └────────────┬────────────────────┘
                                           │ (auth)
                                           ▼
                              ┌─────────────────────────────────┐
                              │    fastestai-playground          │  port 7011
                              │  Auth · Sessions · Payments       │
                              │  Chat · User/Org management       │
                              └────────────┬────────────────────┘
                                           │ (workflow execution)
                                           ▼
                              ┌─────────────────────────────────┐
                              │       fastestai-api              │  port 9394
                              │  Workflow Engine                 │
                              │  LLM Integration (OpenAI/Anthropic/Groq)
                              │  40+ Native Tools                │
                              │  MCP Tool Router (mcpplus.py)    │
                              └──────┬────────────────┬─────────┘
                                     │                │
                         ┌───────────▼──┐   ┌────────▼──────────┐
                         │  MCP Servers │   │   omnimcp-be      │  port 7001
                         │  (direct)    │   │  Tool Discovery    │
                         │              │   │  Vector Index (Qdrant)
                         │  GS-MCP      │   │  Tool Enrichment   │
                         │  excelize-mcp│   └───────────────────┘
                         │  audio-      │             │
                         │  toolkit     │             │ SSE / OpenAPI
                         │  maybe-      │             ▼
                         │  image-gen   │   ┌───────────────────┐
                         │  maybe-      │   │ MCP Servers        │
                         │  video-gen   │   │ (via omnimcp-be)   │
                         └──────────────┘   └───────────────────┘
```

---

## fastestai-api — Workflow Runtime

**Port:** 9394 | **Stack:** Python 3.12+, FastAPI, Redis, MongoDB, Qdrant

### What it does

1. **Workflow execution** — Runs `Workflow → Step → Action → Tool` chains, with SSE streaming
2. **LLM orchestration** — Integrates OpenAI, Anthropic, Groq; supports ReAct agents
3. **Tool routing** — Routes tool calls to MCP servers via `mcpplus.py`
4. **Dataflow DSL** — Declarative alternative to code-based workflows (`ToolCallFlow`, `MapFlow`, `FilterFlow`, `LoopFlow`, `SwitchFlow`, `HumanInteractionFlow`, `ConfluenceFlow`)
5. **Memory** — `mem0ai` + Qdrant for agent memory
6. **Skills** — Skill indexing and retrieval

### Key Modules

| Module | Path | Purpose |
|--------|------|---------|
| Workflow engine | `src/fastestai/workflow/` | Workflow definition, validation, execution, Redis streaming cache |
| Dataflow DSL | `src/fastestai/dataflow/` | Declarative AI workflow definition |
| Agent system | `src/fastestai/agents/` | NLO/ReAct base agents, multi-agent teams, tool execution loops |
| Chat | `src/fastestai/chat/` | Auto chat, Omni chat, dispatch |
| Tools (40+) | `src/fastestai/tools/` | sheet, image, video, code, db_query, google_search, crawler, news_headlines, pandas_ai, etc. |
| MCP routing | `src/fastestai/tools/mcpplus/mcpplus.py` | Bridge between workflow tools and MCP servers |
| Memory | `src/fastestai/memory/` | mem0ai + Qdrant vector store |
| Skill | `src/fastestai/skill/` | Skill indexing and retrieval |

### API Endpoints

```
/health                               → {"message": "ok"}
POST /chat                           → Chat endpoints
POST /workflow                       → Workflow execution (streaming SSE)
/v1/tool/*                          → Tool APIs
/v1/agent/*                         → Agent management & execution
/v1/memory/*                        → Memory management
/v1/skill/*                         → Skill APIs
/v1/internal/*                       → Internal APIs (hidden from docs)
```

### Running

```bash
cd fastestai-api
just install && just dev   # Dev server port 9394 with hot-reload
just api                   # Production server
```

---

## fastestai-playground — Auth & Sessions

**Port:** 7011 | **Stack:** Python, FastAPI, MongoDB (3 instances), Redis, Rye

### What it does

1. **JWT authentication** — User auth, social OAuth (GitHub, Twitter)
2. **VIP/tier management** — Credit system for agents, apps, chat
3. **Chat sessions/threads** — Messaging persistence
4. **Excel via MCP** — Upload/download, formula evaluation via `excelize-mcp`
5. **Payment** — Stripe/PayPal subscriptions

### Key Modules

| Module | Purpose |
|--------|---------|
| `user/` | JWT auth, OAuth, VIP tiers |
| `payment/` | Stripe/PayPal subscriptions |
| `chat/` | Sessions, threads, messages |
| `excel/` | Excel ops via MCP (upload, download, formula eval) |
| `organization/` | Org subscriptions |

### Running

```bash
cd fastestai-playground
just setup && just dev   # Dev server port 7011
just api                 # Production
```

---

## omnimcp-be — Tool Discovery

**Port:** 7001 | **Stack:** Python, FastAPI, MongoDB, Redis, Qdrant

### What it does

1. **MCP server registry** — Register MCP servers via SSE or OpenAPI
2. **Tool discovery** — Auto-index tools from registered servers
3. **Semantic search** — Vector embeddings (OpenAI `ada-002`) stored in Qdrant
4. **Tool enrichment** — LLM generates sample queries, output schemas from request logs
5. **Tool caching** — Redis-backed cache for frequently-used tools

### Data Flow

```
Server Register → MongoDB (mcp_server) → Tool Index
Request Logs → LLM Enrichment → tool_meta → Qdrant Vector Index
Search Query → Pattern + Vector search → Ranked Results
```

### Key Endpoints

```
GET  /mcp/server/detail     → Server status
POST /mcp/server            → Register new server
POST /tool/knowledge/generate → Trigger LLM enrichment
POST /tool/server/tool/reindex → Force reindex
```

### Running

```bash
cd omnimcp-be
uvicorn src.omnimcp_be.app:app --reload --port 7001
```

---

## MCP Routing — mcpplus.py

**File:** `fastestai-api/src/fastestai/tools/mcpplus/mcpplus.py`

This is the **critical integration point** between `fastestai-api` and MCP servers.

### What it does

1. **Transport abstraction** — Routes to SSE or `streamable-http` based on URL pattern
2. **DataFrame/Series conversion** — Bridges high-level types (Polars DataFrames) to MCP primitives
3. **Tool call proxy** — `call_tool_by_sse()` — the main entry point for MCP tool invocation
4. **MCP session management** — Maintains `ClientSession` lifecycle

### Usage Pattern

```python
from fastestai.tools.mcpplus import call_tool_by_sse

result = await call_tool_by_sse(
    sse_url="https://be-dev.omnimcp.ai/api/v1/mcp/key/{server_id}/sse",
    tool_name="google_sheets__write_new_sheet",
    args={"data": df, "sheet_name": "My Sheet"}
)
```

### Active MCP Servers

| Server | Port | Transport | Purpose |
|--------|------|-----------|---------|
| `GS-MCP` | 8321 | `streamable-http` | Google Sheets read/write |
| `excelize-mcp` | 8080 | HTTP | Excel operations |
| `audio-toolkit-mcp` | 8000 | FastMCP | Audio/video/image |
| `maybe-image-generation` | dev | npm | AI image |
| `maybe-text-2-video-generation` | dev | npm | AI video |
| `erp-mcp` | — | FastMCP | Qianyi ERP (27 tools) |
| `pd-smartdatalake` | — | FastMCP | PandasAI natural language Excel |

---

## MCP vs CLI Transport

### MCP (Model Context Protocol)

```
AI Agent → fastestai-api → mcpplus.py → omnimcp-be → MCP Server
```
- **Use when:** AI agent needs to dynamically discover and call tools at runtime
- **Pros:** Tool discovery via semantic search, standardized protocol
- **Cons:** Higher token overhead, more complex routing
- **Transport:** `streamable-http` (preferred), SSE

### CLI (maybeai-app + app-cli)

```
OpenClaw/Agent → cli/app-cli → cli/maybeai-app → fastestai-api
```
- **Use when:** AI needs to execute a known, fixed tool workflow
- **Pros:** Lower token cost, simpler integration, explicit control
- **Cons:** No dynamic tool discovery
- **Preferred for:** AI agent tool consumption (your stated preference)

### Which to Use

| Scenario | Transport |
|----------|-----------|
| AI agent dynamically finds tools | MCP |
| AI executes a known workflow (e.g., image generation) | CLI |
| Human user clicks a button in the UI | MCP |
| OpenClaw invokes a skill | CLI |

---

## Workflow Execution Flow

```
Client → POST /workflow/run
    │
    ├── Validate RunWorkflow model
    ├── Create WorkflowRunner instance
    ├── Initialize workflow
    ├── Prepare tools
    ├── Save initial state → MongoDB
    │
    └── Event loop:
        ├── Get next action
        ├── Check dependencies
        ├── Execute action
        │     └── LLM tool call → mcpplus.py → MCP Server
        ├── Save outputs → MongoDB
        └── Yield WorkflowEvent (SSE) → Client
```

Redis keys for workflow state:
- `workflow:event:{task_id}` — SSE event stream
- `workflow:status:{task_id}` — Task status

---

## Key Files for Tool Integration

| File | Purpose |
|------|---------|
| `fastestai-api/src/fastestai/tools/mcpplus/mcpplus.py` | MCP routing bridge (1345 lines) |
| `omnimcp-be/src/omnimcp_be/mcp/tool/tool_index.py` | Qdrant vector indexing |
| `omnimcp-be/src/omnimcp_be/mcp/tool/tool_knowlege.py` | LLM tool enrichment |
| `fastestai-api/src/fastestai/workflow/` | Workflow execution engine |
| `fastestai-api/src/fastestai/dataflow/` | Dataflow DSL |

---

## Env Vars That Matter

| Service | Key Variable | Purpose |
|---------|-------------|---------|
| `fastestai-api` | `FASTESTAI_API_URL` | Self-reference |
| `fastestai-api` | `TOOL_SERVER` | omnimcp-be URL for tool discovery |
| `fastestai-playground` | `PLAYGROUND_URL` | Self-reference |
| `fastestai-playground` | `EXCELIZE_MCP_URL` | excelize-mcp server URL |
| `omnimcp-be` | `QDRANT_URL` | Vector database |
| `omnimcp-be` | `MONGODB_URI` | Tool metadata storage |

---

*Last updated: 2026-04-20*
