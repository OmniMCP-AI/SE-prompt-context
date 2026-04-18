# Prompt Context Repository

This repository contains prompt context, design documentation, and reference materials for MaybeAI's AI agent system. It is the **shared layer** separate from each submodule's own docs and CLAUDE.md files.

## Repository Index

### 📂 01-product
- [`prd.md`](./01-product/prd.md) — Product requirements (July 2025, historical)
- [`sheet-workflow-ux-design.md`](./01-product/sheet-workflow-ux-design.md) — UX design spec (March 2026)
- [`ecommerce-ai-ux-solution.md`](./01-product/ecommerce-ai-ux-solution.md) — E-commerce UX solution
- [`system-basic-intro.txt`](./01-product/system-basic-intro.txt)
- [`field-template-intro.md`](./01-product/field-template-intro.md)

### 📂 02-architecture
- **design/**
  - [`action-detail-0724.mermaid`](./02-architecture/design/action-detail-0724.mermaid)
  - [`context.mermaid`](./02-architecture/design/context.mermaid)
  - [`workflow-create-2507.mermaid`](./02-architecture/design/workflow-create-2507.mermaid)
  - [`workflow-run-2507.mermaid`](./02-architecture/design/workflow-run-2507.mermaid)
- **resource/**
  - [`Fastest.ai Architecture-2025-06-clean.png`](./02-architecture/resource/Fastest.ai%20Architecture-2025-06-clean.png)
  - [`Fastest.ai-Deployment-2025-06.png`](./02-architecture/resource/Fastest.ai-Deployment-2025-06.png)
  - [`fastestai-tool_agent-workflow.png`](./02-architecture/resource/fastestai-tool_agent-workflow.png)
  - [`omni-leadagent-spawn-new-agent-design.png`](./02-architecture/resource/omni-leadagent-spawn-new-agent-design.png)
- **best-practise-design/**
  - [`12-agent-factors.md`](./02-architecture/best-practise-design/12-agent-factors.md)
  - [`build-multi-agent-research-system.md`](./02-architecture/best-practise-design/build-multi-agent-research-system.md)
  - [`building-effective-agents.md`](./02-architecture/best-practise-design/building-effective-agents.md)
  - [`research_lead_agent.md`](./02-architecture/best-practise-design/research_lead_agent.md)
  - [`research_subagent.md`](./02-architecture/best-practise-design/research_subagent.md)
  - [`SOTA-prompt.txt`](./02-architecture/best-practise-design/SOTA-prompt.txt)

### 📂 03-frontend
- [`requirement.md`](./03-frontend/requirement.md)

### 📂 04-reference
External references and frameworks for AI agent development.
- **context-engineering/** — Making knowledge, memory, and tool context legible for AI agents
  - [`context-erngineering.md`](./04-reference/context-engineering/context-erngineering.md)
  - [`how_to_fix_context.md`](./04-reference/context-engineering/how_to_fix_context.md)
  - [`Agent2Agent.txt`](./04-reference/context-engineering/Agent2Agent.txt)
  - [`Search-R1-Training-LLMs-to-Reason-and-Leverage-Search-Engines-with-Reinforcement-Learning.pdf`](./04-reference/context-engineering/Search-R1-Training-LLMs-to-Reason-and-Leverage-Search-Engines-with-Reinforcement-Learning.pdf)
  - [`writing-a-good-claude-md.md`](./04-reference/context-engineering/writing-a-good-claude-md.md)
  - [`using-claude-md-file.md`](./04-reference/context-engineering/using-claude-md-file.md)
  - [`competitors.md`](./04-reference/context-engineering/competitors.md)
  - **system-prompts-and-models-of-ai-tools/** — External reference (Cursor, Devin, Junie, Lovable, v0, etc.)
- **harness-engineering/** — Agent-first development, feedback loops, evaluation harnesses, agentic CI/CD
  - [`harness-engineering.md`](./04-reference/harness-engineering/harness-engineering.md) — OpenAI Codex agent-first experiment (canonical)
  - [`harness-engineering.html.md`](./04-reference/harness-engineering/harness-engineering.html.md)
  - [`Harness-layer-solution.md`](./04-reference/harness-engineering/Harness-layer-solution.md)
  - [`harness-design-long-running-apps.md`](./04-reference/harness-engineering/harness-design-long-running-apps.md)
  - [`managed-agents.md`](./04-reference/harness-engineering/managed-agents.md)
  - [`sheet-harness-plan.md`](./04-reference/harness-engineering/sheet-harness-plan.md) — Typed spreadsheet output harness (451-line engineering spec)
- **llm-wiki-pattern/** — Persistent compounding knowledge base pattern for LLMs
  - [`llm-wiki.md`](./04-reference/llm-wiki-pattern/llm-wiki.md)

### 📂 05-debug
- [`.gitkeep`](./05-debug/.gitkeep)

### 📂 06-thinking
- [`thinking-pattern-posheli.txt`](./06-thinking/thinking-pattern-posheli.txt)

### 📂 07-coding-rules
- [`coding-guildeline.txt`](./07-coding-rules/coding-guildeline.txt)
- [`no-unnecessary-updates-rule.mdc`](./07-coding-rules/no-unnecessary-updates-rule.mdc)

### 📂 08-process-mgmt
- [`submit-mcp.mermaid`](./08-process-mgmt/submit-mcp.mermaid)
- [`update-mcp-process.mermaid`](./08-process-mgmt/update-mcp-process.mermaid)

### 📂 09-knowledge
- [`crm-erp.json`](./09-knowledge/crm-erp.json)
- [`e-commerce.json`](./09-knowledge/e-commerce.json)
- [`finance.json`](./09-knowledge/finance.json)
- [`recruitment.json`](./09-knowledge/recruitment.json)
- [`social-media.json`](./09-knowledge/social-media.json)
- [`knowledge-domain.txt`](./09-knowledge/knowledge-domain.txt)

### 📂 10-quality
- [`best-practise-tool.md`](./10-quality/best-practise-tool.md)
- [`llm-chosse-the-right-tool.md`](./10-quality/llm-chosse-the-right-tool.md)

### 📂 11-deploy
- [`.justfile`](./11-deploy/.justfile)
- [`jenkins.sh`](./11-deploy/jenkins.sh)
- [`refresh-cache-omni.sh`](./11-deploy/refresh-cache-omni.sh)

### 📂 12-agent
- [`bug-fixer-multi-repo.md`](./12-agent/bug-fixer-multi-repo.md)
- [`code-reviewer.md`](./12-agent/code-reviewer.md)
- [`code-simplifier.md`](./12-agent/code-simplifier.md)
- [`fasttracebug.md`](./12-agent/fasttracebug.md)
- [`performance-optimizer.md`](./12-agent/performance-optimizer.md)
- [`vision-process-agent.md`](./12-agent/vision-process-agent.md)

### 📂 13-skill
- [`traceissue.md`](./13-skill/traceissue.md)

### 📂 14-common-prompt
- [`freq-plan.md`](./14-common-prompt/freq-plan.md)

### 📂 17-ecommerce-wiki
E-commerce workflow reference wiki (plain markdown, no Obsidian required).
- [`index.md`](./17-ecommerce-wiki/index.md)
- [`SCHEMA.md`](./17-ecommerce-wiki/SCHEMA.md)
- [`ecommerce-data-pipeline.md`](./17-ecommerce-wiki/ecommerce-data-pipeline.md)
- [`log.md`](./17-ecommerce-wiki/log.md)
- [`wkly-sample-workflow.json`](./17-ecommerce-wiki/wkly-sample-workflow.json)
- [`e-comm-datapipeline-pattern.xlsx`](./17-ecommerce-wiki/e-comm-datapipeline-pattern.xlsx)

### 📂 docs
Pointers to live user/dev documentation (not stored here — linked only).
- [`image-video-gen-docs.md`](./docs/image-video-gen-docs.md) — Links to `docs.maybe.ai` for AI image/video generation

### 📂 archive
Stale or superseded documents — kept for reference, not for active use.
- **old-design-docs/** — Archived design documents (pre-2025 architecture)
- **old-architecture/** — Archived architecture research docs

### Root Files
- [`.gitignore`](./.gitignore)
- [`llms-full.txt`](./llms-full.txt)
