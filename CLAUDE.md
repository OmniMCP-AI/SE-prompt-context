# CLAUDE.md — SE-prompt-context

> For AI agents (Claude Code, Codex, OpenCode) and developers working in this repository.

## What This Repo Is

**Shared documentation layer** for the maybeai-uni monorepo. It contains:
- Product requirements and UX design docs
- Architecture diagrams and cross-repo patterns
- Domain knowledge (e-commerce, finance, CRM, recruitment)
- Agent prompt templates (bug fixer, code reviewer, etc.)
- Debugging guides and coding standards

It is **not** source code. Each submodule (`fastestai-api`, `mcp/GS-MCP`, etc.) has its own `CLAUDE.md` with service-specific details.

## How to Use This Repo

```
When working in maybeai-uni:
1. Read maybeai-uni/CLAUDE.md first (monorepo entry point)
2. Then read SE-prompt-context/README.md (product/domain context)
3. Then read relevant section in SE-prompt-context/ (your task domain)
4. Then read the submodule's own CLAUDE.md (service details)
```

## Key Entry Points

| File | Purpose |
|------|---------|
| `README.md` | Master index with "when to use what" guidance |
| `01-product/prd.md` | Original PRD (July 2025, historical) |
| `01-product/sheet-workflow-ux-design.md` | UX design spec (March 2026) |
| `maibeiBI/CLAUDE.md` | maibei.maybe.ai product context |

## AI Agent Conventions in This Repo

- **Frontmatter on agent files:** Agent templates in `12-agent/` use YAML frontmatter (`name`, `description`, `skill`, `model`)
- **LLM Wiki pattern:** `04-reference/llm-wiki-pattern/llm-wiki.md` describes the organizing principle — this repo is structured as a wiki
- **Knowledge files:** Domain knowledge in `09-knowledge/` is JSON — read as data, not prose
- **Mermaid diagrams:** Architecture and process flows in `02-architecture/design/` and `08-process-mgmt/`

## Directory Purpose

| Dir | Purpose |
|-----|---------|
| `01-product/` | PRD, UX design, product context |
| `02-architecture/` | Architecture diagrams, design patterns |
| `03-frontend/` | Frontend requirements |
| `04-reference/` | External refs: context eng, harness eng, LLM wiki |
| `07-coding-rules/` | Coding guidelines (minimal: small changes, modular, proper paths) |
| `08-process-mgmt/` | MCP submit/update process diagrams |
| `09-knowledge/` | Domain knowledge JSON |
| `10-quality/` | Tool selection and best practice guides |
| `11-deploy/` | Deployment scripts |
| `12-agent/` | Agent prompt templates |
| `13-skill/` | Skill templates (traceissue) |
| `17-ecommerce-wiki/` | E-commerce workflow reference wiki |
| `docs/` | Pointers to live external docs only |

## MCP vs CLI Transport

- **MCP**: Use for runtime tool discovery — `streamable-http` transport, indexed by omnimcp-be
- **CLI**: Prefer for AI consumption — `cli/maybeai-app` + `cli/app-cli`, lower token cost, simpler control

## Coding Style (from this repo)

- Small, minimal changes
- Abstraction layers to hide implementation details
- Modular, reusable code
- Place files in proper paths according to repo structure

---

*Last updated: 2026-04-20*
