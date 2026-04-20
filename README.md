# MaybeAI — SE Prompt Context

> **Purpose:** Shared documentation layer for AI agents (Claude Code, Codex, OpenCode) and developers working on MaybeAI products. Each submodule has its own `CLAUDE.md` — this repo covers **product context, cross-repo patterns, and domain knowledge** that applies across the monorepo.

---

## 🗂️ How to Navigate This Repo

### For AI Agents: Start Here First

```
When working in maybeai-uni, read these in order:
1. maybeai-uni/CLAUDE.md          ← monorepo entry point (submodules, commands, architecture)
2. SE-prompt-context/README.md     ← you are here (product domain, cross-repo patterns)
3. SE-prompt-context/01-product/  ← product context for your task
4. Relevant submodule/CLAUDE.md    ← service-specific details
```

### For Developers: Start Here First

```
1. maybeai-uni/CLAUDE.md          ← setup, commands, testing
2. SE-prompt-context/README.md    ← you are here (product domain, design context)
3. SE-prompt-context/01-product/  ← product requirements and UX design docs
4. maibeiBI/                      ← maibei.maybe.ai product docs
```

---

## 🏷️ Product Map

> **Status as of 2026-04-20.** Flags: ✅ live, 🔨 active dev, ⚠️ outdated/overpromises

| Product | URL | Status | Notes |
|---------|-----|--------|-------|
| **maibei.maybe.ai** | https://maibei.maybe.ai | ✅ live | Shopee卖家BI — 销售/广告/库存分析, AI Agent驱动 |
| **claw.maybe.ai** | https://claw.maybe.ai | ⚠️ overpromises | Some listed features may not exist yet; check runtime first |
| **maybe.ai** | https://maybe.ai | ⚠️ outdated | Runtime still used for workflow execution; build rarely updated |
| **docs.maybei.ai** | https://docs.maybei.ai | ✅ live | Feishu-hosted user/dev docs (maibei product) |
| **docs.maibei.maybe.ai** | https://docs.maibei.maybe.ai | ✅ live | GitBook API docs for maibei BI |

---

## 🧠 Domain Knowledge

### E-commerce (核心领域)
Shopee 卖家数据运营 — 订单、广告、库存、选品、联盟营销

| File | What It Covers |
|------|---------------|
| `09-knowledge/e-commerce.json` | E-commerce domain entities, metrics, workflows |
| `09-knowledge/crm-erp.json` | CRM/ERP domain knowledge |
| `17-ecommerce-wiki/` | E-commerce workflow reference wiki (schema, data pipeline, sample workflows) |

### Finance & Business Metrics
| File | What It Covers |
|------|---------------|
| `09-knowledge/finance.json` | Revenue, cost, profit calculation patterns |

### Recruitment & Social Media
| File | What It Covers |
|------|---------------|
| `09-knowledge/recruitment.json` | Hiring domain knowledge |
| `09-knowledge/social-media.json` | Social platform data patterns |

---

## 🏗️ Architecture & Cross-Repo Patterns

### Runtime Architecture (start here for system-level understanding)

**`02-architecture/runtime.md`** — Full runtime docs: fastestai-api + fastestai-playground + omnimcp-be stack, MCP routing via mcpplus.py, CLI vs MCP transport comparison, workflow execution flow.

### System Overview

```
User → [Frontend: app-factory/apps/chat]
            ↓
     fastestai-playground (auth, port 7011)
            ↓
     fastestai-api (workflow runtime, port 9394)
            ↓
     ┌── mcpplus.py routes to MCP servers ─────────┐
     │  ├── GS-MCP          (Google Sheets)         │
     │  ├── excelize-mcp    (Excel read/write)      │
     │  ├── audio-toolkit-mcp (media processing)    │
     │  ├── maybe-image-generation                  │
     │  └── maybe-text-2-video-generation           │
     │                                                │
     └── omnimcp-be (tool discovery, port 7001, Qdrant)
              │
              └── omnimcp-api-proxy (OpenAPI → MCP)
```

### Key Integration Files

| File | Role |
|------|------|
| `02-architecture/runtime.md` | **Start here** — full runtime architecture doc |
| `fastestai-api/src/fastestai/tools/mcpplus/mcpplus.py` | Routes all MCP tool calls (1345 lines) |
| `omnimcp-be/` | MCP server discovery + tool indexing |
| `cli/` | maybeai-app API + app-cli — CLI-first tool consumption (token-efficient) |
| `mcp/` | All MCP servers — GS-MCP, excelize-mcp, audio-toolkit, image, video, erp-mcp, etc. |

### MCP vs CLI Transport

- **MCP** (`streamable-http`): For when AI agents need to discover and call tools dynamically at runtime — tool indexing, semantic search via omnimcp-be
- **CLI** (`maybeai-app` + `app-cli`): Preferred for AI consumption — lower token cost, simpler integration, easier to control. Used by OpenClaw, scripts, and direct API calls
- Both transport modes use the same underlying tools — the difference is how tools are invoked

### Design Reference

| File | Covers |
|------|--------|
| `02-architecture/runtime.md` | ⭐ Full runtime architecture — fastestai-api, fastestai-playground, omnimcp-be, mcpplus |
| `02-architecture/design/context.mermaid` | Context flow |
| `02-architecture/design/workflow-create-2507.mermaid` | Workflow creation flow |
| `02-architecture/design/workflow-run-2507.mermaid` | Workflow execution flow |
| `02-architecture/best-practise-design/12-agent-factors.md` | 12 factors for multi-agent systems |
| `04-reference/context-engineering/context-erngineering.md` | Making context legible for AI |
| `04-reference/harness-engineering/harness-engineering.md` | Agent-first dev, feedback loops |

---

## 📋 Product Requirements & UX Design

### maibeiBI (maibei.maybe.ai)

> Shopee seller BI — OAuth-authorized data access, AI-driven analysis and reporting

- **Product overview:** `maibeiBI/website/features.md` — 销售/广告/库存/联盟营销/智能报表
- **API docs:** `maibeiBI/api-docs/` → live at `https://docs.maibei.maybe.ai`
- **Auth:** Shopee OAuth 2.0, multi-store support
- **Data types:** Orders, Products, Shop, Finance, Ads, Affiliate
- **Key metric:** GMV, 毛利率, ACOS, 库存周转天数, 客单价

### PRD (Historical, July 2025)

- `01-product/prd.md` — Original intent framework: 4-layer architecture (Intent Recognition → Planning → Master Agent → Dynamic Tool)
- `01-product/system-basic-intro.txt` — Original product positioning: vibe-coding + workflow automation
- `01-product/sheet-workflow-ux-design.md` — UX spec (March 2026)
- `01-product/ecommerce-ai-ux-solution.md` — E-commerce AI UX solution

### UX & Design Docs

| File | Purpose |
|------|---------|
| `01-product/sheet-workflow-ux-design.md` | Sheet-first workflow UX spec |
| `01-product/ecommerce-ai-ux-solution.md` | E-commerce user experience |
| `maibeiBI/sheet-workflow-ux-design.md` | Duplicate — prefer this path |
| `maibeiBI/ecommerce-ai-ux-solution.md` | Duplicate — prefer this path |

---

## 🔧 Tools & Skills

### MCP Servers (Active)

| Server | Port | Transport | Purpose |
|--------|------|-----------|---------|
| `mcp/GS-MCP` | 8321 | `streamable-http` | Google Sheets read/write |
| `mcp/excelize-mcp` | 8080 | HTTP | Excel operations (openpyxl) |
| `mcp/audio-toolkit-mcp` | 8000 | FastMCP | Audio/video/image processing |
| `mcp/maybe-image-generation` | dev | npm | AI image generation |
| `mcp/maybe-text-2-video-generation` | dev | npm | AI video generation |
| `mcp/erp-mcp` | — | FastMCP | Qianyi ERP (27 tools) |
| `mcp/pd-smartdatalake` | — | FastMCP | Natural language Excel query via PandasAI |

### CLI Stack

| Component | Location | Purpose |
|-----------|----------|---------|
| `maybeai-app` | `cli/maybeai-app/` | FastAPI backend — unified app parameters, workflow dispatch |
| `app-cli` | `cli/app-cli/` | CLI wrapper for maybeai-app |
| `maybeai-image-app` | `cli/app-cli/src/maybeai-image-app.mjs` | Image app CLI command |
| OpenClaw skills | `cli/skills/` | OpenClaw invokes CLI via natural language intent |

### Skills (skillhub/)

Domain-specific reusable skills. Located at `maybeai-uni/skillhub/`.

### Agent Prompts (12-agent/)

| File | Agent Role |
|------|-----------|
| `12-agent/bug-fixer-multi-repo.md` | Debug across fastestai-api + MCP servers, submit PR |
| `12-agent/code-reviewer.md` | Code review agent |
| `12-agent/code-simplifier.md` | Simplify complex code |
| `12-agent/fasttracebug.md` | Fast bug tracing |
| `12-agent/performance-optimizer.md` | Performance optimization |
| `12-agent/vision-process-agent.md` | Vision/image processing agent |

---

## 🚀 Deployment & Operations

| File | Purpose |
|------|---------|
| `11-deploy/.justfile` | Just commands for deployments |
| `11-deploy/jenkins.sh` | Jenkins CI/CD pipeline |
| `11-deploy/refresh-cache-omni.sh` | Cache refresh script |
| `maibeiBI/deploy-demo.sh` | MaibeiBI demo Docker deploy |
| `maibeiBI/docker-compose.yml` | MaibeiBI demo stack |

---

## 🔍 Debugging & Quality

### Debug

| File | Purpose |
|------|---------|
| `maibeiBI/api-docs/configuration/browser-scraper.md` | Browser scraper config for data plugins |
| `10-quality/best-practise-tool.md` | Tool best practices |
| `10-quality/llm-chosse-the-right-tool.md` | LLM tool selection guide |

### Reference: Context Engineering

| File | Purpose |
|------|---------|
| `04-reference/context-engineering/context-erngineering.md` | Making knowledge/context legible for AI |
| `04-reference/context-engineering/how_to_fix_context.md` | Context fixing patterns |
| `04-reference/harness-engineering/harness-engineering.md` | Agent-first dev + feedback loops |
| `04-reference/llm-wiki-pattern/llm-wiki.md` | LLM Wiki pattern — this repo's own organizing principle |

### Archive (do not use actively)

- `archive/old-design-docs/` — pre-2025 architecture
- `archive/old-architecture/` — superseded design docs

---

## 📦 Directory Index

```
SE-prompt-context/
├── 01-product/           # PRD, UX design, product context
├── 02-architecture/      # System architecture diagrams, design patterns
│   ├── design/           # Mermaid diagrams (context, workflow-create/run)
│   ├── resource/         # Architecture PNGs
│   └── runtime.md        # ⭐ Full runtime docs (fastestai-api + omnimcp-be)
├── 03-frontend/           # Frontend requirements
├── 04-reference/          # External references: context engineering, harness eng, LLM wiki
├── 05-debug/              # Debug artifacts (empty)
├── 06-thinking/           # Thinking patterns
├── 07-coding-rules/       # Coding guidelines
├── 08-process-mgmt/       # Process diagrams (MCP submit/update)
├── 09-knowledge/          # Domain knowledge JSON (e-commerce, finance, crm, etc.)
├── 10-quality/            # Quality guides (tool selection, best practices)
├── 11-deploy/             # Deployment scripts & configs
├── 12-agent/              # Agent prompt templates (bug fixer, code reviewer, etc.)
├── 13-skill/              # Skill templates (traceissue)
├── 14-common-prompt/      # Common prompt fragments
├── 17-ecommerce-wiki/     # E-commerce workflow reference wiki
├── docs/                  # Pointers to live external docs only
│   └── image-video-gen-docs.md  # Links to docs.maybe.ai image/video pages
├── archive/               # Stale docs — do not use actively
│   ├── old-design-docs/
│   └── old-architecture/
└── llms-full.txt          # Full context dump (all files concatenated)
```

---

## 📌 Conventions for This Repo

1. **File index in README** — each section lists what files cover and why
2. **"When to use"** guidance — not just what exists, but when to read what
3. **Freshness dating** — files include last-modified context where known
4. **Live docs are linked, not copied** — no duplicate content that can drift
5. **MCP vs CLI distinction** — always clarify which transport to use and why
6. **GitBook vs Feishu** — docs.maybei.ai (Feishu) for maibei user docs; docs.maibei.maybe.ai (GitBook) for maibei API docs

---

*Last updated: 2026-04-20*
