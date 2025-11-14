# Univer Architecture Overview

> A comprehensive guide to understanding Univer's architecture, frontend/backend split, and implementation requirements.

## Table of Contents
- [Project Overview](#project-overview)
- [Frontend vs Backend](#frontend-vs-backend)
- [Core Architecture](#core-architecture)
- [Sheets Feature Packages](#sheets-feature-packages)
- [Formula Engine](#formula-engine)
- [RPC System (Web Workers)](#rpc-system-web-workers)
- [Data Persistence & History](#data-persistence--history)
- [What You Need to Implement](#what-you-need-to-implement)

---

## Project Overview

**Univer is a FRONTEND-FIRST framework** for building spreadsheet, document, and presentation applications that run in the browser.

- **Primary Focus**: Client-side (browser) applications
- **Technology Stack**: React 19, TypeScript, Canvas-based rendering
- **Isomorphic Support**: Can also run in Node.js for headless operations
- **Monorepo**: Uses pnpm workspaces with 60+ packages

---

## Frontend vs Backend

### What is Frontend (Client-Side)

**Everything in the `packages/` directory runs on the client-side (user's browser):**

```
packages/
├── core/                   ← Core framework (DI, models, services)
├── engine-formula/         ← Formula calculation engine
├── engine-render/          ← Canvas rendering engine
├── sheets/                 ← Spreadsheet business logic
├── sheets-ui/              ← Spreadsheet UI components
├── sheets-*/               ← 28 sheets feature packages
├── docs/                   ← Document support
├── slides/                 ← Presentation support
├── ui/                     ← Base UI components
└── ...
```

**All these run in the browser!**

### What is NOT Backend

**There is NO traditional backend/server code in this repository:**

- ❌ No Express/Nest.js server
- ❌ No database integration
- ❌ No REST/GraphQL APIs
- ❌ No persistent storage

### The Confusion: RPC ≠ Backend

**`@univerjs/rpc` and `@univerjs/rpc-node` are NOT backend servers!**

They are for **multi-threading performance optimization**:
- `@univerjs/rpc` → Web Workers in the browser
- `@univerjs/rpc-node` → Worker threads in Node.js
- Both are still **client-side** (no network involved)

---

## Core Architecture

### Technology Stack

```
Frontend Stack:
┌─────────────────────────────────────────┐
│  React 19.2.0                           │
│  TypeScript 5.9.3                       │
│  Vite (build tool)                      │
│  RxJS 7.x (reactive programming)        │
│  Canvas API (rendering)                 │
│  @wendellhu/redi (dependency injection) │
└─────────────────────────────────────────┘
```

### Package Dependencies

```
Core Foundation:
packages/core (base framework)
    ↓
Engine Layer:
├── packages/engine-formula (formula calculation)
└── packages/engine-render (canvas rendering)
    ↓
Business Logic:
packages/sheets (spreadsheet core)
    ↓
UI Layer:
packages/sheets-ui (UI components)
    ↓
Feature Plugins:
├── packages/sheets-formula
├── packages/sheets-conditional-formatting
├── packages/sheets-data-validation
└── ... (25+ more feature packages)
```

---

## Sheets Feature Packages

### Core Sheets Packages

1. **`packages/sheets`** - Core spreadsheet functionality
   - Cells, rows, columns, worksheets, workbooks
   - Business logic, no UI

2. **`packages/sheets-ui`** - Main UI components
   - Spreadsheet interface
   - User interactions

3. **`packages/engine-formula`** - Formula calculation
   - 350+ Excel-compatible functions
   - Dependency tracking
   - Runs in main thread or Web Worker

4. **`packages/engine-render`** - Rendering engine
   - Canvas-based rendering
   - High performance
   - Browser only (needs Canvas API)

5. **`packages/core`** - Base framework
   - Dependency injection
   - Plugin system
   - Shared across all document types

### Feature Packages (Architecture Pattern)

Each feature follows a consistent pattern:

**Base Package** (business logic, no UI):
- `packages/sheets-formula/`
- `packages/sheets-filter/`
- `packages/sheets-data-validation/`
- etc.

**UI Package** (user interface):
- `packages/sheets-formula-ui/`
- `packages/sheets-filter-ui/`
- `packages/sheets-data-validation-ui/`
- etc.

### All 28 Sheets Packages

```
Core:
- sheets                    ← Core spreadsheet
- sheets-ui                 ← UI components

Features:
- sheets-formula            - sheets-formula-ui
- sheets-filter             - sheets-filter-ui
- sheets-sort               - sheets-sort-ui
- sheets-data-validation    - sheets-data-validation-ui
- sheets-conditional-formatting - sheets-conditional-formatting-ui
- sheets-table              - sheets-table-ui
- sheets-numfmt             - sheets-numfmt-ui
- sheets-hyper-link         - sheets-hyper-link-ui
- sheets-note               - sheets-note-ui
- sheets-drawing            - sheets-drawing-ui
- sheets-thread-comment     - sheets-thread-comment-ui

Single Package Features:
- sheets-find-replace
- sheets-crosshair-highlight
- sheets-zen-editor
- sheets-graphics
```

---

## Formula Engine

### What It Is

`@univerjs/engine-formula` is a **complete spreadsheet formula calculation engine** running entirely in JavaScript:

```
packages/engine-formula/src/
├── engine/
│   ├── analysis/       ← Lexer & Parser (formula parsing)
│   ├── ast-node/       ← Abstract Syntax Tree
│   ├── dependency/     ← Dependency tracking
│   ├── interpreter/    ← Formula execution
│   └── value-object/   ← Value types
├── functions/
│   ├── array/          ← Array functions
│   ├── date/           ← Date/Time (TODAY, NOW, etc.)
│   ├── financial/      ← Financial (NPV, IRR, etc.)
│   ├── logical/        ← IF, AND, OR, etc.
│   ├── lookup/         ← VLOOKUP, INDEX, MATCH, etc.
│   ├── math/           ← SUM, AVERAGE, etc.
│   ├── statistical/    ← Statistical functions
│   ├── text/           ← Text manipulation
│   └── web/            ← Web functions
└── services/           ← Runtime services
```

### How It Works

```
Formula Input: "=SUM(A1:A10)"
    ↓
Lexer: Tokenize
    ↓
Parser: Build AST
    ↓
Dependency Tracker: Track A1:A10
    ↓
Interpreter: Execute SUM function
    ↓
Result: 55
```

### Where It Runs

**100% Client-Side** (with flexibility):

```
Browser Main Thread:
┌─────────────────────────┐
│  Formula Engine         │
│  - Parse formulas       │
│  - Calculate results    │
└─────────────────────────┘

OR (for better performance)

Browser Web Worker:
┌─────────────────────────┐
│  Formula Engine         │
│  - Heavy calculations   │
│  - No UI blocking       │
└─────────────────────────┘

OR (for headless operations)

Node.js Process:
┌─────────────────────────┐
│  Formula Engine         │
│  - Server-side calc     │
│  - API manipulation     │
└─────────────────────────┘
```

**Key Point**: All three environments are **client-side** or **headless** - there's no traditional "backend server" involved!

---

## RPC System (Web Workers)

### What RPC Actually Does

**RPC = Remote Procedure Call** but it's **NOT server-side**!

It enables **multi-threading in the browser** for performance optimization.

### Architecture Comparison

#### ❌ What People Think (WRONG):

```
Browser ──HTTP──> Backend Server
                  └─ Formula calculation
```

#### ✅ What It Actually Is (CORRECT):

```
Browser (Same Computer, Same Process)
├─ Main Thread (UI)
│  - Rendering
│  - User interactions
│  - Canvas drawing
│
└─ Web Worker Thread (Calculations)
   - Formula engine
   - Heavy computations
   - No UI access

Communication: postMessage() (in-memory, instant)
```

### How Web Workers Work

**Main Thread** (`examples/src/sheets/main.ts`):
```typescript
// Create a Web Worker (still in browser!)
const worker = new Worker(new URL('./worker.js', import.meta.url));

univer.registerPlugins([
    [UniverRPCMainThreadPlugin, { workerURL: worker }],
    [UniverSheetsPlugin, {
        notExecuteFormula: true  // Don't calculate in main thread
    }],
    // ... UI plugins
]);
```

**Web Worker Thread** (`examples/src/sheets/worker.ts`):
```typescript
// This runs in a separate thread (still in browser!)
const univer = new Univer({ /* config */ });

univer.registerPlugins([
    [UniverFormulaEnginePlugin],     // Calculate formulas HERE
    [UniverRPCWorkerThreadPlugin],   // Communicate with main thread
    // NO UI plugins (workers can't access DOM)
]);
```

### Benefits

| Without Web Worker | With Web Worker |
|-------------------|-----------------|
| Heavy formula calculation freezes UI | UI stays responsive |
| User must wait for calculations | User can keep working |
| Single-threaded | Multi-threaded |
| Poor UX on large datasets | Smooth performance |

### Key Differences

```
❌ Server-Side (NOT what RPC does):
Browser ──HTTP/WebSocket──> Server (different computer)
                             └─ Node.js process
                             └─ Database
                             └─ APIs

✅ Web Worker (What RPC actually does):
Browser (same computer)
  ├─ Main Thread (UI)
  └─ Worker Thread (calculations)
       ↕ postMessage() - in-memory, no network!
```

---

## Data Persistence & History

### What's Built-In (Frontend Only)

#### ✅ 1. Snapshot/Save to JSON

Location: `packages/sheets/src/facade/f-workbook.ts:125-138`

```typescript
const workbook = univerAPI.getActiveWorkbook();
const snapshot = workbook.save();  // Returns IWorkbookData
console.log(snapshot);             // Complete workbook JSON
```

**Features**:
- Returns complete workbook data as JSON
- Includes: cells, formulas, formatting, styles, plugins
- Location: In-memory only
- **Not persistent**: Lost on page refresh

#### ✅ 2. Undo/Redo History

Location: `packages/core/src/services/undoredo/undoredo.service.ts`

```typescript
// Built-in undo/redo
commandService.executeCommand(UndoCommand.id);
commandService.executeCommand(RedoCommand.id);
```

**Features**:
- Full undo/redo system
- Tracks all mutations (edits, formatting, etc.)
- Location: In-memory only
- **Lost on refresh**: Not persisted

#### ✅ 3. Resource Manager

Location: `packages/core/src/services/resource-manager/resource-manager.service.ts`

**Features**:
- Serializes plugin data for saving
- Returns JSON representation
- **Not persistent**: Just provides data

### What's NOT Built-In

#### ❌ 1. Database Persistence
- No built-in database integration
- No auto-save functionality
- No backend API calls

#### ❌ 2. Version History Storage
- Undo/redo is in-memory only
- No version history storage
- No "restore previous version" feature

#### ❌ 3. Collaboration/Real-time Sync
- Collaboration is in the **paid non-OSS version** only
- OSS version has NO collaboration backend
- Must implement yourself or purchase

---

## What You Need to Implement

### Backend Architecture

```
┌─────────────────────────────────────────────────┐
│  Browser (Univer OSS)                           │
│  ├─ User edits spreadsheet                      │
│  ├─ workbook.save() → IWorkbookData (JSON)     │
│  └─ YOU implement: Send to backend              │
└──────────────────┬──────────────────────────────┘
                   │
                   │ HTTP POST / WebSocket
                   │ (You implement this)
                   ↓
┌─────────────────────────────────────────────────┐
│  YOUR Backend (You must implement!)            │
│  ├─ REST API / GraphQL / WebSocket              │
│  ├─ Database (PostgreSQL, MongoDB, etc.)        │
│  ├─ Version history (if needed)                 │
│  ├─ User authentication                         │
│  └─ Collaboration (if needed)                   │
└─────────────────────────────────────────────────┘
```

### Implementation Example

#### Frontend (Your Code)

```typescript
import { FUniver } from '@univerjs/core/facade';

const univerAPI = FUniver.newAPI(univer);
const workbook = univerAPI.getActiveWorkbook();

// 1. Save snapshot
const snapshot = workbook.save();  // IWorkbookData

// 2. Send to YOUR backend
await fetch('/api/workbooks/save', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: workbook.getId(),
    data: snapshot,
    timestamp: new Date().toISOString()
  })
});

// 3. Auto-save (You implement)
let autoSaveTimer;
univerAPI.onCommandExecuted((command) => {
  clearTimeout(autoSaveTimer);
  autoSaveTimer = setTimeout(async () => {
    const snapshot = workbook.save();
    await saveToBackend(snapshot);
  }, 2000); // Auto-save after 2s of inactivity
});

// 4. Load from YOUR backend
const response = await fetch('/api/workbooks/123');
const savedData = await response.json();

// 5. Restore workbook
univerAPI.createWorkbook(savedData.data);
```

#### Backend Example (Node.js/Express)

```typescript
// Save workbook
app.post('/api/workbooks/:id/save', async (req, res) => {
  const { id } = req.params;
  const { data, timestamp } = req.body;

  // Save current version to database
  await db.workbooks.upsert({
    id: id,
    data: data,
    updatedAt: timestamp,
    userId: req.user.id
  });

  res.json({ success: true });
});

// Load workbook
app.get('/api/workbooks/:id', async (req, res) => {
  const workbook = await db.workbooks.findById(req.params.id);
  res.json(workbook);
});

// Version history (You implement)
app.post('/api/workbooks/:id/versions', async (req, res) => {
  const { id } = req.params;
  const { data } = req.body;

  // Save as new version
  await db.workbookVersions.create({
    workbookId: id,
    version: await getNextVersion(id),
    data: data,
    createdAt: new Date(),
    userId: req.user.id
  });

  res.json({ success: true });
});

// Get version history
app.get('/api/workbooks/:id/history', async (req, res) => {
  const versions = await db.workbookVersions.find({
    workbookId: req.params.id
  }).sort({ version: -1 }).limit(50);

  res.json(versions);
});

// Restore version
app.post('/api/workbooks/:id/restore/:version', async (req, res) => {
  const { id, version } = req.params;

  const versionData = await db.workbookVersions.findOne({
    workbookId: id,
    version: parseInt(version)
  });

  // Restore as current
  await db.workbooks.update(id, {
    data: versionData.data,
    updatedAt: new Date()
  });

  res.json(versionData);
});
```

### Feature Checklist

| Feature | Built-in? | Location | What You Need |
|---------|-----------|----------|---------------|
| **Save to JSON** | ✅ Yes | Frontend | Nothing |
| **Undo/Redo** | ✅ Yes | Frontend (in-memory) | Nothing |
| **Load from JSON** | ✅ Yes | Frontend | Nothing |
| **Database persistence** | ❌ No | - | Backend API + Database |
| **Auto-save** | ❌ No | - | Frontend timer + Backend endpoint |
| **Version history** | ❌ No | - | Backend versioning system |
| **User authentication** | ❌ No | - | Auth system (JWT, OAuth, etc.) |
| **Collaboration** | ❌ No (paid only) | - | WebSocket + OT/CRDT OR paid version |
| **File export (XLSX)** | ❌ No (paid only) | - | Backend library OR paid version |
| **File import (XLSX)** | ❌ No (paid only) | - | Backend library OR paid version |

---

## Summary

### Key Takeaways

1. **Univer is 100% frontend** - Everything runs in the browser
2. **No backend included** - You must build your own persistence layer
3. **RPC ≠ Backend** - It's just Web Workers for performance
4. **Formula engine is client-side** - Can run in browser or Node.js
5. **Collaboration is paid** - OSS version has no built-in collaboration
6. **You own persistence** - Must implement save/load/history yourself

### For Sheets Development

If you're focusing on **sheets features**, you'll work primarily with:

```
packages/sheets/           ← Your main focus
packages/sheets-ui/        ← UI components
packages/sheets-*/         ← Feature-specific packages
packages/engine-formula/   ← When working with formulas
packages/core/             ← Framework fundamentals
```

**All frontend development** - No backend code needed unless you're building the persistence layer!

---

## Additional Resources

- [Official Documentation](https://docs.univer.ai)
- [GitHub Repository](https://github.com/dream-num/univer)
- [Examples](https://docs.univer.ai/showcase)
- [Web Worker Architecture](https://docs.univer.ai/guides/recipes/architecture/web-worker)

---

**Last Updated**: 2025-01-14
**Univer Version**: 0.10.14
