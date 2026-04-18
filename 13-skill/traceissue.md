# Trace Issue Skill

Analyze logs from tracer.fastest.ai to identify root causes of issues in the Maybe AI system.

## Arguments

- `$ARGUMENTS` - Required: Task ID (UUID format) and optional bug description

## Instructions

You are analyzing logs to identify the root cause of an issue. Follow these steps:

### Step 1: Parse Input

Extract from `$ARGUMENTS`:
- **Task ID**: A UUID like `522ef9fb-8f4e-4428-9b20-afa89b0909ec`
- **Bug Description**: Optional additional context about the issue

If no valid Task ID is found, ask the user to provide one.

### Step 2: Retrieve Logs

**IMPORTANT**: You MUST use the `mcp__crawlUrl__crawlUrl` tool to fetch error logs from tracer.fastest.ai.

**Container to Repository Mapping**:
| Container (indice) | Repository |
|--------------------|------------|
| `fastest-api*` | `fastestai-api` at `/Users/dengwei/work/ai/om3/fastestai-api` |
| `play-be` | `fastestai-playground` at `/Users/dengwei/work/ai/om3/fastestai-playground` |

**Step 2a: Fetch Error Logs**

Call the `mcp__crawlUrl__crawlUrl` tool with this exact URL format (replace `{task_id}` with the actual task ID):

```
mcp__crawlUrl__crawlUrl(url="https://tracer.fastest.ai/?keyword={task_id}&type=error-function&indice=fastest-api*&indice=play-be")
```

Example with real task ID:
```
mcp__crawlUrl__crawlUrl(url="https://tracer.fastest.ai/?keyword=522ef9fb-8f4e-4428-9b20-afa89b0909ec&type=error-function&indice=fastest-api*&indice=play-be")
```

This retrieves:
- **Errors** from `fastest-api` container (repo: `fastestai-api`)
- **Exceptions** from `fastest-api` container
- **Function calls** from `fastest-api` container
- **Errors/Exceptions/Function calls** from `play-be` container (repo: `fastestai-playground`)

**Step 2b: If more context needed, fetch all logs from fastest-api**:

```
mcp__crawlUrl__crawlUrl(url="https://tracer.fastest.ai/?keyword={task_id}&type=all&indice=fastest-api")
```

**URL Parameters**:
- `keyword`: The task ID (UUID)
- `type`: Log type filter (`error-function` for errors/exceptions/function calls, `all` for everything)
- `indice`: Container/service name (can specify multiple with `&indice=...`)

### Step 3: Parse and Analyze Logs

Look for these key signals in the logs:
- **Errors**: `"level": "error"` entries
- **Exceptions**: Stack traces in the `exception` field
- **Tool Call Errors**: Events like `"Tool call error"`
- **Function Calls**: To understand the workflow sequence

### Step 4: Classify the Error

Identify the error type:
1. **Timeout** - Contains `CALL_TOOL_TIMEOUT`, `timeout`, `TimeoutError`
2. **Invalid Parameter** - Contains `InvalidParameter`, `422`, `validation error`
3. **API Error** - Contains `status 400`, `status 500`, `API failed`
4. **Import Error** - Contains `ImportError`, `ModuleNotFoundError`
5. **Data Format Error** - Contains `JSONDecodeError`, `KeyError`, `TypeError`
6. **MCP Tool Error** - MCP-specific failures in tool execution
7. **Unknown** - Other errors

### Step 5: Map to Repository

**MCP Tool Naming Convention**: `{server_name}__{tool_name}`

Example: `maybe_image_generation__recognize_image`
- Server: `maybe_image_generation`
- Tool: `recognize_image`

**Repository Mappings**:
| Server Name | Repository Path |
|-------------|-----------------|
| `maybe_image_generation` | `/Users/dengwei/work/ai/om3/mcp/ads3-mcp-server/apps/maybe-image-generation` |
| `maybe_text_2_video_generation` | `/Users/dengwei/work/ai/om3/mcp/ads3-mcp-server/apps/maybe-text-2-video-generation` |
| `excelize` | `/Users/dengwei/work/ai/om3/mcp/excelize-mcp` |
| `gs_mcp` | `/Users/dengwei/work/ai/om3/mcp/GS-MCP` |
| `audio_toolkit` | `/Users/dengwei/work/ai/om3/mcp/audio-toolkit-mcp` |

**Core System Repositories**:
| Index/Service | Repository Path |
|---------------|-----------------|
| `fastest-api` | `/Users/dengwei/work/ai/om3/fastestai-api` |
| `play-be` | `/Users/dengwei/work/ai/om3/fastestai-playground` |
| `omnimcp-be` | `/Users/dengwei/work/ai/om3/omnimcp-be` |
| `omnimcp-api-proxy` | `/Users/dengwei/work/ai/om3/omnimcp-api-proxy` |

**Key File in fastest-api**:
- MCP Tool Calls: `/Users/dengwei/work/ai/om3/fastestai-api/src/fastestai/tools/mcpplus/mcpplus.py`

### Step 6: Extract Code Context

If the error contains a traceback:
1. Parse file paths and line numbers from the traceback
2. Read the relevant source files
3. Identify the specific function/line causing the issue

### Step 7: Provide Root Cause Summary

Present your findings in this format:

```
## Root Cause Analysis

**Task ID**: {task_id}

**Error Type**: {classification}

**Summary**: {one-line description}

**Affected Services**: {list of services from log indices}

**Failure Location**:
- Repository: {repo_path}
- File: {file_path}
- Line: {line_number}
- Function: {function_name}

**Error Details**:
{relevant error message or exception}

**Suggested Fix Approach**:
{based on error type, suggest how to fix}

**Confidence**: {High/Medium/Low}

**Next Steps**:
1. {action item 1}
2. {action item 2}
```

## Error-Specific Fix Approaches

- **Timeout**: Increase timeout settings, add retry logic, optimize slow operations
- **Invalid Parameter**: Validate inputs, check API documentation, add parameter sanitization
- **API Error**: Check API status, review request format, handle edge cases
- **Import Error**: Install missing dependencies, fix import paths
- **Data Format Error**: Add data validation, handle null/empty cases, fix type conversions
- **MCP Tool Error**: Check MCP server health, review tool implementation

## Example Usage

```
/traceissue 522ef9fb-8f4e-4428-9b20-afa89b0909ec Image generation timeout
```

This will analyze logs for the given task ID and provide a root cause analysis focusing on image generation timeout issues.
