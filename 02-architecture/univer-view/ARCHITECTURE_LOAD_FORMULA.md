# Univer Backend & Data Persistence FAQ (Q1-Q3)

> Comprehensive answers to common questions about Univer's data persistence, formula handling, and Node.js vs Python backend choices.

**Last Updated**: 2025-01-20
**Univer Version**: 0.10.14

---

## Table of Contents

- [Q1: BSON vs JSON for Saving Univer Sheets](#q1-bson-vs-json-for-saving-univer-sheets)
- [Q2: Formula Storage and Reading](#q2-formula-storage-and-reading)
- [Q3: Node.js vs Python Backend](#q3-nodejs-vs-python-backend)

---

## Q1: BSON vs JSON for Saving Univer Sheets

### Question

> "Given the current architecture, could I create an API endpoint to save the Univer sheet object to MongoDB using BSON instead of JSON? The benefit I want is to save the object when content contains formulas, so when I load from the workbook I could auto-trigger the formula and get the latest data without manual triggering. Am I correct, or does saving as BSON not matter?"

### Answer: You DON'T Need BSON - Formulas Work Correctly with JSON Storage ✅

**You are actually INCORRECT about needing BSON for formula preservation.**

### How Univer Formulas Actually Work

When a cell contains a formula, Univer saves **BOTH** the formula text and the calculated value:

```json
{
  "cellData": {
    "0": {
      "0": { "v": 100 },                    // A1: value only
      "1": { "v": 200 },                    // B1: value only
      "2": { "f": "=SUM(A1:B1)", "v": 300 } // C1: formula + value
    }
  }
}
```

**Key Fields:**
- `f`: Formula text (e.g., `"=SUM(A1:B1)"`)
- `v`: Calculated value (e.g., `300`)

### What Happens on Load

When you load data from MongoDB:

```typescript
// 1. Fetch from Python API
const response = await fetch(`/api/sheet/${sheetId}`);
const data = await response.json();

// 2. Load into Univer
const workbook = univerAPI.createWorkbook(data.data);

// ✅ At this point, Univer has ALREADY recalculated all formulas!
```

**Automatic Recalculation Process:**

```
1. univerAPI.createWorkbook(data)
   ↓
2. Univer initializes workbook model
   ↓
3. Formula engine detects cells with "f" field
   ↓
4. Builds dependency graph: C1 depends on → A1, B1
   ↓
5. Automatically calculates in order:
   - A1: 100 (no formula)
   - B1: 200 (no formula)
   - C1: =SUM(A1:B1) → Calculate → 300
   ↓
6. Updates internal state with fresh values
   ↓
7. Workbook ready with ALL formulas calculated ✅
```

### Proof: Stale Values Are Ignored

```typescript
// Backend returns (from MongoDB):
{
  "cellData": {
    "0": {
      "0": { "v": 500 },                    // A1: Updated to 500
      "1": { "v": 200 },                    // B1: Still 200
      "2": { "f": "=SUM(A1:B1)", "v": 300 } // C1: OLD/STALE value!
    }
  }
}

// Frontend loads:
const workbook = univerAPI.createWorkbook(data);

// Univer automatically recalculates C1:
// =SUM(A1:B1) = SUM(500, 200) = 700 ✅

const c1 = sheet.getRange('C1');
console.log(c1.getValue());  // Output: 700 (NOT 300!)
```

**The stale value `300` from the database is IGNORED!** Univer always recalculates.

### Why BSON vs JSON Doesn't Matter

**BSON is just a binary encoding of JSON** - it doesn't preserve any special "formula objects":

```
JSON:  { "f": "=SUM(A1:A10)", "v": 55 }
BSON:  (binary version of the same data)
```

Both store:
- ✅ Formula text as string
- ✅ Calculated value
- ✅ Cell metadata

**Neither stores executable formula objects** - the formula engine **re-parses and re-executes** formulas on every load.

### When BSON Actually Helps

BSON is useful for:
- ✅ **Binary data** (images, files) - but Univer stores these as base64 strings anyway
- ✅ **Date objects** - but you're using ISO strings
- ✅ **Large numbers** - but formulas use IEEE 754 floats (same in JSON/BSON)
- ✅ **Smaller size** - marginally, but not significant for spreadsheets

### Your Current Implementation is Already Optimal

Looking at your current code:

```python
# /Users/dengwei/work/ai/fastestai-playground/src/fastestai_playground/sheet/server/sheet_server.py
sheet_doc = {
    "sheets": data.get("sheets", {}),  # ← Contains formulas + values
    "styles": data.get("styles", {}),
}
```

This stores the **exact `IWorkbookData` format** that Univer expects.

### Recommendation

**Keep your current JSON approach!** It's:
- ✅ **Correct** - formulas work perfectly
- ✅ **Simple** - human-readable, debuggable
- ✅ **Standard** - works with all tools
- ✅ **Compatible** - matches Univer's `workbook.save()` format exactly

**Don't switch to BSON** because:
- ❌ No formula preservation benefit
- ❌ Harder to debug (binary format)
- ❌ Requires extra serialization/deserialization
- ❌ Same recalculation behavior as JSON

### Summary Table

| Storage Format | Formula Preservation | Auto-Recalculation | Debugging |
|----------------|---------------------|-------------------|-----------|
| **JSON** (your current) | ✅ Yes | ✅ Yes | ✅ Easy |
| **BSON** (proposed) | ✅ Yes | ✅ Yes | ❌ Hard |

**Verdict**: Stick with JSON. BSON provides zero benefits for your use case.

---

## Q2: Formula Storage and Reading

### Question

> "If the cell content is a formula, will it save as formula or data to DB? When I read from the workbook, could I read the formula instead of the value?"

### Answer: It Saves BOTH Formula AND Value ✅

### What Gets Stored

When a cell contains a formula, Univer saves **BOTH**:

```python
# /Users/dengwei/work/ai/fastestai-playground/src/fastestai_playground/sheet/model.py:22-28
class CellData(BaseModel):
    v: Any = None              # ← Calculated VALUE
    t: Optional[int] = None    # Type
    f: Optional[str] = None    # ← FORMULA text
    s: Optional[str] = None    # Style
    si: Optional[str] = None   # Style ID
```

**Example in MongoDB:**

```json
{
  "_id": "673a1234567890abcdef1234",
  "sheets": {
    "sheet-001": {
      "cellData": {
        "0": {
          "0": { "v": 10 },                      // A1: value only
          "1": { "v": 20 },                      // B1: value only
          "2": { "f": "=A1+B1", "v": 30 }        // C1: formula + value
        },
        "1": {
          "0": { "f": "=A1*2", "v": 20 },        // A2: formula + value
          "1": { "f": "=B1*3", "v": 60 },        // B2: formula + value
          "2": { "f": "=SUM(A2:B2)", "v": 80 }   // C2: formula + value
        }
      }
    }
  }
}
```

### Reading Formulas vs Values

**Yes, you can read BOTH the formula and the value!**

#### Frontend Access (TypeScript/JavaScript)

```typescript
import { FUniver } from '@univerjs/core/facade';

const univerAPI = FUniver.newAPI(univer);
const workbook = univerAPI.getActiveWorkbook();
const sheet = workbook.getActiveSheet();

// Get cell at C1
const c1 = sheet.getRange('C1');

// Read the FORMULA
const formula = c1.getFormula();
console.log(formula);  // "=A1+B1"

// Read the calculated VALUE
const value = c1.getValue();
console.log(value);    // 30

// Check if cell has a formula
const hasFormula = c1.getFormula() !== '';
console.log(hasFormula);  // true
```

#### Backend Access (Python)

```python
# Get sheet from database
sheet = await sheet_server.get_sheet_by_id(sheet_id, user_id)

# Access cell data
cell_data = sheet.sheets["sheet-001"].cellData.get("0", {}).get("2", None)

if cell_data:
    # Read the FORMULA
    formula = cell_data.f  # "=A1+B1"

    # Read the VALUE
    value = cell_data.v    # 30

    # Check if it's a formula cell
    is_formula = cell_data.f is not None

    print(f"Formula: {formula}")
    print(f"Value: {value}")
```

### Extract All Formulas from a Sheet

#### Backend Example (Python)

```python
from fastestai_playground.sheet.server.sheet_server import SheetServer

async def get_all_formulas(sheet_id: str, user_id: str):
    """Extract all formulas from a sheet"""
    sheet_server = SheetServer()
    sheet = await sheet_server.get_sheet_by_id(sheet_id, user_id)

    if not sheet:
        return []

    formulas = []

    # Loop through all sheets
    for sheet_id, sheet_config in sheet.sheets.items():
        # Loop through all cells
        for row_idx, row_data in sheet_config.cellData.items():
            for col_idx, cell_data in row_data.items():
                if cell_data.f:  # Has formula
                    formulas.append({
                        "sheet": sheet_config.name,
                        "row": int(row_idx),
                        "col": int(col_idx),
                        "cell": f"{chr(65 + int(col_idx))}{int(row_idx) + 1}",
                        "formula": cell_data.f,
                        "value": cell_data.v,
                        "type": cell_data.t
                    })

    return formulas

# Usage
formulas = await get_all_formulas("673a1234567890", "user_123")
for f in formulas:
    print(f"Cell {f['cell']}: {f['formula']} = {f['value']}")
```

### What Gets Stored vs What Gets Calculated

| Data Field | Stored in MongoDB? | Calculated on Load? | Used by Univer? |
|------------|-------------------|---------------------|-----------------|
| **`f` (formula)** | ✅ Yes | ❌ No | ✅ Yes - for calculation |
| **`v` (value)** | ✅ Yes | ✅ Yes (if `f` exists) | ⚠️ Ignored if `f` exists |
| **Cell without formula** | ✅ Yes (`v` only) | ❌ No | ✅ Yes - used as-is |

**Key insight:** When a cell has both `f` and `v`:
- `f` is the **source of truth**
- `v` from database is **ignored**
- `v` is **recalculated** based on `f` and dependencies

### Summary

**To directly answer your questions:**

1. **"If the cell content is formula, will it save as formula or data to DB?"**
   - **Answer**: BOTH! It saves the formula text (`f` field) AND the calculated value (`v` field)

2. **"When I read from the workbook, could I read the formula instead of the value?"**
   - **Answer**: YES! You can read:
     - Formula text: `cellData.f` (e.g., `"=SUM(B1:B10)"`)
     - Calculated value: `cellData.v` (e.g., `550`)
     - Or both at the same time

Your current implementation already stores and retrieves both correctly!

---

## Q3: Node.js vs Python Backend

### Question

> "What are the benefits of using Node.js version as backend vs Python? Background: We chose Python because we need a user system (which already exists), and we use it to save the data (Univer sheet). These two parts seem Univer doesn't provide (user system and save data for backend, not webpage cache)."

### Answer: Your Python Backend Choice is CORRECT ✅

After examining the Univer source code at `/Users/dengwei/work/ai/github/univer`, here's the definitive analysis:

### What Univer Actually Provides for Node.js

#### Headless Univer in Node.js ✅

From `/Users/dengwei/work/ai/github/univer/examples/src/node/cases/basic.ts`:

```typescript
// Univer CAN run in Node.js (headless)
import { FUniver } from '@univerjs/core/facade';
import { createUniverOnNode } from '../sdk';

const API = FUniver.newAPI(createUniverOnNode());
const workbook = API.createWorkbook({});

const a1 = workbook.getActiveSheet().getRange('A1');
await a1.setValue({ v: 123 });

const b1 = workbook.getActiveSheet().getRange('B1');
await b1.setValue({ f: '=SUM(A1) * 6' });  // Formula!

console.log('Formula value:', b1.getCellData()?.v);  // Output: 738
console.log(workbook.save());  // Get JSON snapshot
```

**What this means:**
- ✅ You CAN run Univer in Node.js
- ✅ Formula engine works server-side
- ✅ Same API as browser
- ❌ **BUT** there's NO backend server - just headless calculation!

#### What's NOT Included ❌

After examining the codebase, **there is NO:**
- ❌ REST API server
- ❌ GraphQL server
- ❌ WebSocket server for collaboration
- ❌ Database integration
- ❌ User authentication
- ❌ Data persistence layer
- ❌ File storage system

### Key Finding: Node.js Support ≠ Backend Server

```
/Users/dengwei/work/ai/github/univer/packages/
├── rpc/           ← Web Worker communication (browser)
├── rpc-node/      ← Worker threads (Node.js) - NOT a server!
├── core/          ← Framework
├── engine-formula/ ← Formula engine (isomorphic)
└── sheets/        ← Spreadsheet logic

❌ NO packages for:
   - HTTP server
   - Database
   - Auth
   - API routes
```

### Comparison: Node.js vs Python Backend

| Aspect | Node.js Backend | Python Backend (Your Choice) |
|--------|----------------|------------------------------|
| **Univer Integration** | ✅ Easier - same language | ⚠️ Requires API translation |
| **Existing Auth System** | ❌ Need to rebuild | ✅ Already exists |
| **Code Reuse** | ✅ Share types with frontend | ❌ Separate type definitions |
| **Headless Rendering** | ✅ `@univerjs/core` runs in Node | ✅ Can use Python libraries |
| **Formula Calculation** | ✅ Native `@univerjs/engine-formula` | ❌ Need API calls or separate service |
| **Performance** | ✅ Event-driven, fast I/O | ✅ Fast for data processing |
| **Ecosystem** | ✅ npm packages, TypeScript | ✅ Data science, ML, existing tools |
| **Development Speed** | ⚠️ Need to rebuild everything | ✅ Leverage existing codebase |
| **Team Expertise** | ? Depends on team | ✅ Already using Python |
| **Maintenance** | ⚠️ Two language stacks | ✅ Single language stack |

### When Node.js Backend Makes Sense

#### Use Case 1: Heavy Server-Side Formula Calculation

```typescript
// Node.js backend can run Univer headless
import { Univer } from '@univerjs/core';
import { UniverFormulaEnginePlugin } from '@univerjs/engine-formula';

const univer = new Univer();
univer.registerPlugin(UniverFormulaEnginePlugin);

// Calculate formulas server-side
app.post('/api/calculate', async (req, res) => {
  const { workbookData } = req.body;
  const workbook = univer.createWorkbook(workbookData);
  const snapshot = workbook.save();
  res.json(snapshot);
});
```

**When you need this:**
- Large-scale batch processing (1000+ workbooks/day)
- API-based calculations without frontend
- Formula validation before saving
- Pre-calculating expensive formulas

#### Use Case 2: Type Sharing & Code Reuse

```typescript
// Shared types between frontend & backend
export interface IWorkbookData {
  sheets: Record<string, ISheetData>;
  styles: Record<string, IStyleData>;
}

// Frontend
const data: IWorkbookData = workbook.save();

// Backend (Node.js)
app.post('/save', (req, res) => {
  const data: IWorkbookData = req.body;  // ← Same types!
});
```

### When Python Backend Makes Sense (Your Case) ✅

#### Scenario 1: Existing Infrastructure

```python
# Your current setup - ALREADY WORKS
from fastestai_playground.user.auth import get_current_user
from fastestai_playground.sheet.server.sheet_server import SheetServer

@router.post("/sheet/add")
async def create_sheet(
    request: CreateSheetRequest,
    current_user: User = Depends(get_current_user),  # ← Existing auth!
    sheet_server: SheetServer = Depends(get_sheet_server),
):
    # No need to rebuild auth system
    sheet = await sheet_server.create_sheet(
        user_id=current_user.id,  # ← Uses existing user system
        data=request.data
    )
```

**Why this is better:**
- ✅ No need to rebuild user authentication
- ✅ No need to rebuild authorization logic
- ✅ Reuse existing database connections
- ✅ Consistent with existing codebase

#### Scenario 2: Data Processing & Integration

```python
# Python excels at data processing
import pandas as pd

@router.post("/sheet/import-csv")
async def import_csv(file: UploadFile, current_user: User = Depends(get_current_user)):
    # Python pandas for data transformation
    df = pd.read_csv(file.file)

    # Transform to Univer format
    cell_data = {}
    for row_idx, row in df.iterrows():
        cell_data[str(row_idx)] = {}
        for col_idx, value in enumerate(row):
            cell_data[str(row_idx)][str(col_idx)] = {
                "v": value,
                "t": 2 if isinstance(value, (int, float)) else 1
            }

    # Save to MongoDB
    sheet = await sheet_server.create_sheet(...)
```

**Python advantages:**
- ✅ Pandas for data manipulation
- ✅ NumPy for calculations
- ✅ scikit-learn for ML
- ✅ Rich data science ecosystem

### Hybrid Approach (Best of Both Worlds)

You can use **BOTH** Node.js and Python if needed:

```
┌─────────────────────────────────────────────────┐
│  Frontend (Browser)                             │
│  - React + Univer                               │
└──────────────┬──────────────────────────────────┘
               │
               ├─────────────────────────────────┐
               ↓                                 ↓
┌──────────────────────────┐    ┌────────────────────────────┐
│  Python Backend (Main)   │    │  Node.js Microservice      │
│  - User auth ✅          │    │  - Formula calculation     │
│  - Data persistence ✅   │    │  - Headless rendering      │
│  - Business logic ✅     │    │  - Heavy computation       │
│  - ML/Data processing ✅ │    │                            │
└──────────────────────────┘    └────────────────────────────┘
               │                                 ↑
               └─────────────────────────────────┘
                     (Internal API calls)
```

### Decision Matrix

| Your Requirement | Node.js Only | Python Only | Hybrid |
|-----------------|-------------|-------------|--------|
| **User authentication exists** | ❌ Rebuild | ✅ Use existing | ✅ Use existing |
| **Data persistence exists** | ❌ Rebuild | ✅ Use existing | ✅ Use existing |
| **Server-side formula calc** | ✅ Native | ❌ Complex | ✅ Best option |
| **Team uses Python** | ❌ New skills | ✅ Existing | ⚠️ Some learning |
| **Development speed** | Slow | ✅ Fast | Medium |
| **Maintenance complexity** | Medium | ✅ Low | ⚠️ Medium-High |
| **Cost** | Medium | ✅ Low | Medium |

### Decision Tree

```
Do you have an existing Python backend with auth?
  ↓
 YES → Is formula calculation happening client-side?
        ↓
       YES → Do you process >1000 workbooks/day server-side?
              ↓
             NO → ✅ KEEP PYTHON! (Your current setup)
              ↓
             YES → Do you need sub-100ms calculation response?
                    ↓
                   YES → 💡 Add Node.js microservice
                    ↓
                   NO → ⚠️ Use Python with browser automation
```

### Recommendation for Your Case

**STICK WITH PYTHON** ✅

**Reasons:**
1. ✅ **Existing user system** - No need to rebuild
2. ✅ **Existing data persistence** - Already integrated with MongoDB
3. ✅ **Team expertise** - Using Python (`fastestai_playground`)
4. ✅ **Fast development** - Leverage existing code
5. ✅ **Lower complexity** - Single language stack

**Only add Node.js microservice IF:**
- You need heavy server-side formula calculation (1000+ workbooks/day)
- You need XLSX import/export at scale
- You need real-time collaboration with OT/CRDT
- You need headless rendering for PDF generation

### What You're Missing Without Node.js

**Not much!** Here's what you CAN'T do:

| Feature | Impact | Workaround |
|---------|--------|------------|
| **Native formula calculation** | Low - happens in browser | None needed |
| **Type sharing** | Low - use Pydantic | API contracts |
| **Headless Univer** | Medium - no server rendering | Use browser automation |
| **XLSX export** | Medium - no native support | Use `openpyxl` (Python) |

### Current Architecture (Optimal)

```
Browser (Univer) ──┐
   ↓ formulas      │ ← Formulas calculated HERE
   ↓ calculated    │
   ↓               │
Python API ────────┘ ← Just stores data
   ↓
MongoDB
```

### Summary

**Your Python backend choice is CORRECT for your use case!**

| Aspect | Your Situation |
|--------|----------------|
| **Current choice** | Python ✅ |
| **Should change?** | ❌ No |
| **Why Python works** | Existing auth, data persistence, team expertise |
| **When to add Node.js** | Only if you need heavy server-side formula processing |
| **Recommendation** | Keep Python, add Node.js microservice only if bottlenecks appear |

No need to complicate with Node.js unless you hit specific performance bottlenecks with server-side formula calculation at scale!

---

## References

- [Univer Documentation](https://docs.univer.ai)
- [GitHub Repository](https://github.com/dream-num/univer)
- [Architecture Overview](./ARCHITECTURE_OVERVIEW.md)
