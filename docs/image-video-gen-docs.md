# MaybeAI Image & Video Generation — Developer & AI Agent Docs

> **Status: 2026-04-20** — Verify feature availability before assuming it exists.
> For user-facing docs, link to live docs below. For internal implementation, refer to source code.

---

## Live User/Dev Documentation

| Feature | Docs URL | AI Agent Note |
|---------|----------|---------------|
| **AI Image Generation** | `https://docs.maybe.ai/image-generation` | User guide, API reference, best practices |
| **AI Video Generation** | `https://docs.maybe.ai/video-generation` | User guide, prompt engineering, output formats |

---

## Internal Implementation Reference

### Image Generation MCP
- **Source:** `maybeai-uni/mcp/maybe-image-generation/`
- **Start:** `npm install && npm run dev`
- **Skill:** `maybeai-uni/skillhub/maybe-image-generation/SKILL.md` (if exists)
- **Transport:** `streamable-http` (MCP) — preferred for runtime tool discovery

### Video Generation MCP
- **Source:** `maybeai-uni/mcp/maybe-text-2-video-generation/`
- **Start:** `npm install && npm run dev`
- **Skill:** `maybeai-uni/skillhub/maybe-text-2-video-generation/SKILL.md` (if exists)
- **Transport:** `streamable-http` (MCP)

---

## Key Workflow Files

Reference workflows for image→video pipelines:

| File | Purpose |
|------|---------|
| `maybeai-uni/key-workflow/1-image-model-try-on.json` | Image try-on workflow |
| `maybeai-uni/key-workflow/2-video-prompt-gen.json` | Video prompt generation |
| `maybeai-uni/key-workflow/3-regerate-9grid-image.json` | 9-grid image regeneration |
| `maybeai-uni/key-workflow/4-generate-video-from-image.json` | Image to video |
| `maybeai-uni/key-workflow/5-concat-video.json` | Video concatenation |

## Excel Templates

| File | Purpose |
|------|---------|
| `maybeai-uni/key-excel/grid_image_video_prompt.xlsx` | Grid image/video prompt template |
| `maybeai-uni/key-excel/step3_success_case.xlsx` | Step 3 success case reference |

---

## For AI Agents

When a user asks about image or video generation:
1. Link to the **live docs** above for user-facing guidance
2. For internal tool implementation, refer to the MCP server code in `mcp/maybe-image-generation/` and `mcp/maybe-text-2-video-generation/`
3. For skill patterns, see `maybeai-uni/skillhub/` for existing SKILL.md files

---

*Last updated: 2026-04-20* — check live docs for latest feature availability
