# MaybeAI Image & Video Generation — User & Developer Docs

> **Purpose:** Link to live user/dev documentation for MaybeAI's AI image and video generation features.
> This file is a pointer. The actual docs live at the marketing/docs site.

---

## Live Documentation

| Feature | Docs URL | Purpose |
|---------|----------|---------|
| **AI Image Generation** | `https://docs.maybe.ai/image-generation` | User guide, API reference, best practices |
| **AI Video Generation** | `https://docs.maybe.ai/video-generation` | User guide, prompt engineering, output formats |

---

## Quick Reference (Internal)

### Image Generation MCP
- Location: `maybeai-uni/mcp/maybe-image-generation/`
- Entry point: `npm run dev` (port dev)
- SKILL.md: `maybeai-uni/skillhub/maybe-image-generation/SKILL.md` (if exists)

### Video Generation MCP
- Location: `maybeai-uni/mcp/maybe-text-2-video-generation/`
- Entry point: `npm run dev`
- SKILL.md: `maybeai-uni/skillhub/maybe-text-2-video-generation/SKILL.md` (if exists)

### Key Workflow Files (Reference)
- `maybeai-uni/key-workflow/1-image-model-try-on.json`
- `maybeai-uni/key-workflow/2-video-prompt-gen.json`
- `maybeai-uni/key-workflow/3-regerate-9grid-image.json`
- `maybeai-uni/key-workflow/4-generate-video-from-image.json`
- `maybeai-uni/key-workflow/5-concat-video.json`

### Excel Templates (Reference)
- `maybeai-uni/key-excel/grid_image_video_prompt.xlsx`
- `maybeai-uni/key-excel/step3_success_case.xlsx`

---

## For LLM / AI Agents

When a user asks about image or video generation:
1. Link to the live docs above for user-facing guidance
2. For internal tool implementation, refer to the MCP server code in `mcp/maybe-image-generation/` and `mcp/maybe-text-2-video-generation/`
3. For skill patterns, see `skillhub/` for existing skill SKILL.md files

---

*Last updated: 2026-04-19*
