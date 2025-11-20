# Univer Images & Charts Integration Guide

> Complete guide for inserting images and charts into Univer sheets, with MCP tool integration and storage strategies.

**Last Updated**: 2025-01-20
**Univer Version**: 0.10.14

---

## Table of Contents

- [Overview](#overview)
- [What Univer Supports](#what-univer-supports)
- [Image Source Types](#image-source-types)
- [Inserting Images - Frontend](#inserting-images---frontend)
- [Inserting Images - Backend API](#inserting-images---backend-api)
- [Chart Generation & Insertion](#chart-generation--insertion)
- [Storage Strategies](#storage-strategies)
- [MCP Tool Integration](#mcp-tool-integration)
- [Complete Workflow Example](#complete-workflow-example)
- [Best Practices](#best-practices)

---

## Overview

Univer provides comprehensive support for inserting images into spreadsheets. While charts are a paid feature in Univer Pro, you can **generate charts as images** using Python libraries (matplotlib, plotly) and insert them into sheets.

### Key Capabilities

✅ **Images** - Fully supported in OSS version
✅ **Charts** - Generate as images, then insert
✅ **Shapes** - Basic shapes supported
❌ **Native Charts** - Paid feature only (`@univerjs-pro/charts`)

---

## What Univer Supports

Based on the Univer source code:

| Feature | Supported? | Package | Notes |
|---------|-----------|---------|-------|
| **Float Images** | ✅ Yes | `@univerjs/sheets-drawing` | Images that float over cells |
| **Cell Images** | ✅ Yes | `@univerjs/sheets-drawing` | Images embedded in cells |
| **Charts** | ⚠️ Paid Only | `@univerjs-pro/charts` | NOT in OSS version |
| **Shapes** | ✅ Yes | `@univerjs/drawing` | Rectangles, circles, etc. |

### Package Structure

```
packages/
├── drawing/              ← Base drawing functionality
├── sheets-drawing/       ← Spreadsheet drawing logic
├── sheets-drawing-ui/    ← UI for inserting images
└── (charts - paid only)  ← Not available in OSS
```

---

## Image Source Types

From `/Users/dengwei/work/ai/github/univer/packages/core/src/services/image-io/image-io.service.ts`:

```typescript
export enum ImageSourceType {
    /**
     * HTTP/HTTPS URLs
     * Example: https://example.com/image.png
     */
    URL = 'URL',

    /**
     * Univer image hosting service ID
     * (Paid service)
     */
    UUID = 'UUID',

    /**
     * Base64 encoded image data
     * Example: data:image/png;base64,iVBORw0KGg...
     */
    BASE64 = 'BASE64',
}
```

### Comparison

| Type | Pros | Cons | Use Case |
|------|------|------|----------|
| **BASE64** | ✅ Self-contained, works offline | ❌ Large document size | Small images (<100KB) |
| **URL** | ✅ Small document, CDN-friendly | ❌ Requires external storage | Large images, production |
| **UUID** | ✅ Managed hosting | ❌ Paid service only | Univer Pro users |

---

## Inserting Images - Frontend

### Method 1: User Upload (Interactive)

From `/Users/dengwei/work/ai/github/univer/packages/sheets-drawing-ui/src/commands/commands/insert-image.command.ts`:

```typescript
import { FUniver } from '@univerjs/core/facade';
import { InsertFloatImageCommand } from '@univerjs/sheets-drawing-ui';

// Get Univer API
const univerAPI = FUniver.newAPI(univer);

// Insert image from File object
const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'image/*';
fileInput.onchange = async (e) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) {
    // Execute insert image command
    await univerAPI.executeCommand(InsertFloatImageCommand.id, {
      files: [file]
    });
  }
};
fileInput.click();
```

### Method 2: Programmatic Insert (Base64)

```typescript
import { FUniver } from '@univerjs/core/facade';

const univerAPI = FUniver.newAPI(univer);
const workbook = univerAPI.getActiveWorkbook();
const sheet = workbook.getActiveSheet();

// Create image data structure
const imageData = {
  drawingId: 'image_' + Date.now(),
  drawingType: 1, // 1 = Image
  imageSourceType: 'BASE64',
  source: 'data:image/png;base64,iVBORw0KGg...', // Your base64 image
  transform: {
    width: 200,
    height: 150,
    angle: 0,
    flipX: false,
    flipY: false
  },
  sheetTransform: {
    from: {
      row: 0,      // Start at cell A1
      column: 0,
      rowOffset: 0,
      columnOffset: 0
    },
    to: {
      row: 5,      // End at cell F6 (spans 5 rows)
      column: 5,   // (spans 5 columns)
      rowOffset: 0,
      columnOffset: 0
    }
  },
  anchorType: '1'  // "0"=Position only, "1"=Both, "2"=None
};

// Add to workbook resources
const snapshot = workbook.save();
snapshot.resources.push({
  name: 'SHEET_DRAWING_PLUGIN',
  data: JSON.stringify({
    [sheet.getSheetId()]: {
      [imageData.drawingId]: imageData
    }
  })
});

// Reload workbook with image
const newWorkbook = univerAPI.createWorkbook(snapshot);
```

### Method 3: Insert from URL

```typescript
// Insert image from external URL
const imageFromUrl = {
  drawingId: 'image_url_' + Date.now(),
  drawingType: 1,
  imageSourceType: 'URL',
  source: 'https://example.com/chart.png',  // ← External URL
  transform: {
    width: 400,
    height: 300,
    angle: 0,
    flipX: false,
    flipY: false
  },
  sheetTransform: {
    from: { row: 0, column: 0, rowOffset: 0, columnOffset: 0 },
    to: { row: 10, column: 8, rowOffset: 0, columnOffset: 0 }
  }
};

// Add to resources (same as above)
```

---

## Inserting Images - Backend API

### Data Models (Python)

```python
# models.py
from pydantic import BaseModel, Field
from typing import Optional, Literal

class ImageTransform(BaseModel):
    """Image transformation properties"""
    width: float
    height: float
    angle: float = 0
    flipX: bool = False
    flipY: bool = False

class SheetPosition(BaseModel):
    """Cell position in sheet"""
    row: int
    column: int
    rowOffset: float = 0
    columnOffset: float = 0

class SheetTransform(BaseModel):
    """Image position on sheet"""
    from_: SheetPosition = Field(..., alias="from")
    to: SheetPosition

class ImageData(BaseModel):
    """Complete image data structure"""
    drawingId: str
    drawingType: int = 1  # 1 = Image
    imageSourceType: Literal["URL", "UUID", "BASE64"]
    source: str  # Image URL or base64 data
    transform: ImageTransform
    sheetTransform: SheetTransform
    anchorType: str = "1"  # "0"=Position, "1"=Both, "2"=None

class InsertImageRequest(BaseModel):
    """Request to insert image"""
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    position: dict = {"row": 0, "column": 0}
    size: dict = {"width": 200, "height": 150}
```

### API Endpoint

```python
# api.py
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import json
from bson import ObjectId

router = APIRouter(prefix="/sheet", tags=["sheet"])

@router.post("/{sheet_id}/insert-image")
async def insert_image(
    sheet_id: str,
    request: InsertImageRequest,
    current_user: User = Depends(get_current_user),
    sheet_server: SheetServer = Depends(get_sheet_server),
):
    """
    Insert image into sheet

    Args:
        sheet_id: Sheet ID
        request: Image data (URL or base64)

    Returns:
        Success response with drawing_id
    """
    # 1. Get existing sheet
    sheet = await sheet_server.get_sheet_by_id(sheet_id, current_user.id)
    if not sheet:
        raise HTTPException(404, "Sheet not found")

    # 2. Validate image source
    if request.image_url:
        source_type = "URL"
        source = request.image_url
    elif request.image_base64:
        source_type = "BASE64"
        source = request.image_base64
    else:
        raise HTTPException(400, "Either image_url or image_base64 required")

    # 3. Create drawing ID
    drawing_id = f"image_{int(datetime.utcnow().timestamp() * 1000)}"

    # 4. Create image data structure
    image_data = ImageData(
        drawingId=drawing_id,
        imageSourceType=source_type,
        source=source,
        transform=ImageTransform(
            width=request.size["width"],
            height=request.size["height"]
        ),
        sheetTransform=SheetTransform(
            **{
                "from": SheetPosition(
                    row=request.position["row"],
                    column=request.position["column"]
                ),
                "to": SheetPosition(
                    row=request.position["row"] + 5,
                    column=request.position["column"] + 3
                )
            }
        )
    )

    # 5. Update sheet resources
    drawing_resource = None
    for resource in sheet.resources:
        if resource.name == "SHEET_DRAWING_PLUGIN":
            drawing_resource = resource
            break

    # Get first sheet ID
    sheet_config_id = list(sheet.sheets.keys())[0]

    if drawing_resource:
        # Update existing resource
        drawing_data = json.loads(drawing_resource.data)
        if sheet_config_id not in drawing_data:
            drawing_data[sheet_config_id] = {}
        drawing_data[sheet_config_id][drawing_id] = image_data.dict(by_alias=True)
        drawing_resource.data = json.dumps(drawing_data)
    else:
        # Create new resource
        drawing_data = {
            sheet_config_id: {
                drawing_id: image_data.dict(by_alias=True)
            }
        }
        sheet.resources.append(
            SheetResource(
                name="SHEET_DRAWING_PLUGIN",
                data=json.dumps(drawing_data)
            )
        )

    # 6. Save to MongoDB
    update_data = {
        "resources": [r.dict() for r in sheet.resources],
        "updated_at": datetime.utcnow()
    }

    await sheet_server.collection.update_one(
        {"_id": ObjectId(sheet_id), "user_id": current_user.id},
        {"$set": update_data}
    )

    return {
        "success": True,
        "drawing_id": drawing_id,
        "message": "Image inserted successfully"
    }
```

---

## Chart Generation & Insertion

Since charts are not available in Univer OSS, generate them as images:

### Using Matplotlib

```python
# chart_service.py
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict

def generate_bar_chart(
    data: List[Dict[str, any]],
    title: str = "Chart",
    figsize: tuple = (10, 6)
) -> str:
    """
    Generate bar chart and return as base64

    Args:
        data: [{"label": "Jan", "value": 100}, ...]
        title: Chart title
        figsize: Figure size (width, height)

    Returns:
        Base64 encoded PNG image
    """
    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    # Create chart
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(labels, values, color='steelblue')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Category')
    ax.set_ylabel('Value')
    ax.grid(True, alpha=0.3)

    # Add value labels on bars
    for i, v in enumerate(values):
        ax.text(i, v + max(values) * 0.02, str(v),
                ha='center', va='bottom')

    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return f"data:image/png;base64,{image_base64}"

def generate_line_chart(data: List[Dict], title: str = "Line Chart") -> str:
    """Generate line chart"""
    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(labels, values, marker='o', linewidth=2, markersize=8)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return f"data:image/png;base64,{image_base64}"

def generate_pie_chart(data: List[Dict], title: str = "Pie Chart") -> str:
    """Generate pie chart"""
    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(title, fontsize=16, fontweight='bold')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return f"data:image/png;base64,{image_base64}"
```

### Chart Insertion API

```python
# api.py (continued)
@router.post("/{sheet_id}/insert-chart")
async def insert_chart(
    sheet_id: str,
    chart_type: Literal["bar", "line", "pie"],
    data: List[Dict[str, any]],
    title: str = "Chart",
    position: dict = {"row": 0, "column": 0},
    current_user: User = Depends(get_current_user),
    sheet_server: SheetServer = Depends(get_sheet_server),
):
    """
    Generate chart and insert into sheet

    Args:
        sheet_id: Sheet ID
        chart_type: "bar", "line", or "pie"
        data: Chart data [{"label": "Jan", "value": 100}, ...]
        title: Chart title
        position: Cell position
    """
    # 1. Generate chart image
    if chart_type == "bar":
        image_base64 = generate_bar_chart(data, title)
    elif chart_type == "line":
        image_base64 = generate_line_chart(data, title)
    elif chart_type == "pie":
        image_base64 = generate_pie_chart(data, title)
    else:
        raise HTTPException(400, f"Unsupported chart type: {chart_type}")

    # 2. Insert as image
    return await insert_image(
        sheet_id=sheet_id,
        request=InsertImageRequest(
            image_base64=image_base64,
            position=position,
            size={"width": 600, "height": 400}
        ),
        current_user=current_user,
        sheet_server=sheet_server
    )
```

---

## Storage Strategies

### Option 1: Base64 in MongoDB (Simple)

**Use for:** Small images (<100KB)

```python
# Stored directly in MongoDB
{
  "_id": "673a123...",
  "resources": [
    {
      "name": "SHEET_DRAWING_PLUGIN",
      "data": '{"sheet-001": {"image_123": {"source": "data:image/png;base64,iVBORw..."}}}'
    }
  ]
}
```

**Pros:**
- ✅ Simple - everything in one place
- ✅ No external dependencies
- ✅ Works offline
- ✅ Atomic operations

**Cons:**
- ❌ Large document size
- ❌ MongoDB 16MB document limit
- ❌ Slower queries
- ❌ Not scalable (>10 images)

### Option 2: External Storage + URL (Recommended)

**Use for:** Production, large images, many images

```python
# storage_service.py
import boto3
from typing import BinaryIO
import uuid

class ImageStorageService:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'your-bucket-name'
        self.cdn_base = 'https://cdn.example.com'

    async def upload_image(
        self,
        image_data: bytes,
        filename: str,
        content_type: str = 'image/png'
    ) -> str:
        """
        Upload image to S3 and return CDN URL

        Returns:
            CDN URL: https://cdn.example.com/images/abc123.png
        """
        # Generate unique filename
        image_id = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        key = f"sheet-images/{image_id}.{extension}"

        # Upload to S3
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=image_data,
            ContentType=content_type,
            ACL='public-read'
        )

        # Return CDN URL
        return f"{self.cdn_base}/{key}"

    async def delete_image(self, image_url: str) -> bool:
        """Delete image from S3"""
        # Extract key from URL
        key = image_url.replace(self.cdn_base + '/', '')

        self.s3.delete_object(Bucket=self.bucket, Key=key)
        return True

# Updated API endpoint
@router.post("/{sheet_id}/insert-image-from-file")
async def insert_image_from_file(
    sheet_id: str,
    file: UploadFile,
    position: dict = {"row": 0, "column": 0},
    current_user: User = Depends(get_current_user),
    storage: ImageStorageService = Depends(get_storage_service),
):
    """Upload image to S3 and insert URL into sheet"""
    # 1. Upload to S3
    image_data = await file.read()
    image_url = await storage.upload_image(
        image_data=image_data,
        filename=file.filename,
        content_type=file.content_type
    )

    # 2. Insert URL reference
    return await insert_image(
        sheet_id=sheet_id,
        request=InsertImageRequest(
            image_url=image_url,  # ← URL, not base64
            position=position,
            size={"width": 400, "height": 300}
        ),
        current_user=current_user
    )
```

**MongoDB storage:**
```json
{
  "_id": "673a123...",
  "resources": [
    {
      "name": "SHEET_DRAWING_PLUGIN",
      "data": '{"sheet-001": {"image_123": {"source": "https://cdn.example.com/images/abc.png", "imageSourceType": "URL"}}}'
    }
  ]
}
```

**Pros:**
- ✅ Small MongoDB documents
- ✅ Fast queries
- ✅ Scalable to 1000s of images
- ✅ CDN support
- ✅ Image optimization possible

**Cons:**
- ❌ Requires external storage (S3, Azure, GCS)
- ❌ More complex setup
- ❌ Additional costs

### Option 3: Hybrid Approach (Smart)

**Best of both worlds:**

```python
# Smart storage decision
MAX_BASE64_SIZE = 100_000  # 100KB threshold

async def insert_image_smart(
    sheet_id: str,
    image_data: bytes,
    filename: str,
    position: dict,
    current_user: User,
    storage: ImageStorageService
):
    """
    Smart storage: small = base64, large = S3
    """
    if len(image_data) < MAX_BASE64_SIZE:
        # Small image: embed as base64
        base64_data = base64.b64encode(image_data).decode()
        return await insert_image(
            sheet_id=sheet_id,
            request=InsertImageRequest(
                image_base64=f"data:image/png;base64,{base64_data}",
                position=position
            ),
            current_user=current_user
        )
    else:
        # Large image: upload to S3
        image_url = await storage.upload_image(image_data, filename)
        return await insert_image(
            sheet_id=sheet_id,
            request=InsertImageRequest(
                image_url=image_url,
                position=position
            ),
            current_user=current_user
        )
```

---

## MCP Tool Integration

### MCP Tool Wrapper

```python
# mcp_tools/sheet_image_tools.py
from typing import Optional, Literal, List, Dict
import httpx

async def mcp_insert_image(
    sheet_id: str,
    image_url: str,
    position: Dict[str, int] = {"row": 0, "column": 0},
    size: Dict[str, int] = {"width": 400, "height": 300},
    user_token: str = None
) -> str:
    """
    MCP tool: Insert image into Univer sheet

    Args:
        sheet_id: Sheet ID
        image_url: URL to image
        position: {"row": 0, "column": 0}
        size: {"width": 400, "height": 300}
        user_token: Auth token

    Returns:
        Success message with drawing_id
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://your-api/sheet/{sheet_id}/insert-image",
            json={
                "image_url": image_url,
                "position": position,
                "size": size
            },
            headers={"Authorization": f"Bearer {user_token}"}
        )
        result = response.json()

        if result["success"]:
            return f"Image inserted successfully at row {position['row']}, column {position['column']}. Drawing ID: {result['drawing_id']}"
        else:
            return f"Failed to insert image: {result.get('message', 'Unknown error')}"

async def mcp_generate_and_insert_chart(
    sheet_id: str,
    chart_type: Literal["bar", "line", "pie"],
    data: List[Dict[str, any]],
    title: str = "Chart",
    position: Dict[str, int] = {"row": 0, "column": 0},
    user_token: str = None
) -> str:
    """
    MCP tool: Generate chart and insert into sheet

    Args:
        sheet_id: Sheet ID
        chart_type: "bar", "line", or "pie"
        data: [{"label": "Jan", "value": 100}, ...]
        title: Chart title
        position: Cell position
        user_token: Auth token

    Returns:
        Success message with chart details
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://your-api/sheet/{sheet_id}/insert-chart",
            json={
                "chart_type": chart_type,
                "data": data,
                "title": title,
                "position": position
            },
            headers={"Authorization": f"Bearer {user_token}"},
            timeout=30.0  # Chart generation may take time
        )
        result = response.json()

        if result["success"]:
            return f"{chart_type.capitalize()} chart '{title}' inserted at row {position['row']}, column {position['column']}"
        else:
            return f"Failed to insert chart: {result.get('message', 'Unknown error')}"
```

---

## Complete Workflow Example

### Scenario: Sales Report with Chart

```python
# workflow/sales_report.py
from typing import List, Dict
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/workflow", tags=["workflow"])

@router.post("/create-sales-report")
async def create_sales_report(
    sheet_id: str,
    sales_data: List[Dict[str, any]],
    current_user: User = Depends(get_current_user),
):
    """
    Complete workflow: Create sales report with chart

    Steps:
    1. Insert sales data into sheet
    2. Generate sales chart
    3. Insert chart into sheet
    4. Return summary
    """
    # 1. Prepare sales data
    months = [d["month"] for d in sales_data]
    sales = [d["sales"] for d in sales_data]

    # 2. Update sheet with data
    sheet = await sheet_server.get_sheet_by_id(sheet_id, current_user.id)

    # Insert data into cells (A1:B12)
    for i, (month, sale) in enumerate(zip(months, sales)):
        row = str(i + 1)
        sheet.sheets["sheet-001"].cellData[row] = {
            "0": {"v": month, "t": 1},  # Column A: Month
            "1": {"v": sale, "t": 2}     # Column B: Sales
        }

    # Add total formula
    total_row = str(len(sales) + 1)
    sheet.sheets["sheet-001"].cellData[total_row] = {
        "0": {"v": "TOTAL", "t": 1},
        "1": {"f": f"=SUM(B1:B{len(sales)})", "t": 2}
    }

    # Save data updates
    await sheet_server.update_sheet(
        sheet_id=sheet_id,
        user_id=current_user.id,
        data={"sheets": sheet.sheets}
    )

    # 3. Generate and insert chart
    chart_result = await insert_chart(
        sheet_id=sheet_id,
        chart_type="bar",
        data=sales_data,
        title="Monthly Sales Report",
        position={"row": 0, "column": 4},  # Column E
        current_user=current_user
    )

    # 4. Return summary
    return {
        "success": True,
        "message": "Sales report created successfully",
        "data": {
            "total_sales": sum(sales),
            "average_sales": sum(sales) / len(sales),
            "best_month": months[sales.index(max(sales))],
            "chart_id": chart_result["drawing_id"],
            "data_range": f"A1:B{len(sales) + 1}",
            "chart_position": "E1"
        }
    }
```

---

## Best Practices

### 1. Image Size Optimization

```python
from PIL import Image
import io

def optimize_image(image_data: bytes, max_size: int = 1024) -> bytes:
    """
    Optimize image size while maintaining quality

    Args:
        image_data: Original image bytes
        max_size: Maximum width/height

    Returns:
        Optimized image bytes
    """
    img = Image.open(io.BytesIO(image_data))

    # Resize if too large
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # Save optimized
    buffer = io.BytesIO()
    img.save(buffer, format='PNG', optimize=True, quality=85)
    return buffer.getvalue()
```

### 2. Error Handling

```python
@router.post("/{sheet_id}/insert-chart")
async def insert_chart_with_error_handling(
    sheet_id: str,
    chart_type: str,
    data: List[Dict],
    current_user: User = Depends(get_current_user),
):
    """Insert chart with comprehensive error handling"""
    try:
        # Validate data
        if not data or len(data) == 0:
            raise HTTPException(400, "Chart data cannot be empty")

        if not all("label" in d and "value" in d for d in data):
            raise HTTPException(400, "Each data point must have 'label' and 'value'")

        # Validate chart type
        if chart_type not in ["bar", "line", "pie"]:
            raise HTTPException(400, f"Unsupported chart type: {chart_type}")

        # Generate chart
        try:
            if chart_type == "bar":
                image_base64 = generate_bar_chart(data)
            elif chart_type == "line":
                image_base64 = generate_line_chart(data)
            else:
                image_base64 = generate_pie_chart(data)
        except Exception as e:
            logger.error(f"Chart generation failed: {str(e)}")
            raise HTTPException(500, f"Failed to generate chart: {str(e)}")

        # Insert image
        return await insert_image(
            sheet_id=sheet_id,
            request=InsertImageRequest(image_base64=image_base64),
            current_user=current_user
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(500, "Internal server error")
```

### 3. Caching Generated Charts

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def generate_cached_chart(
    chart_type: str,
    data_hash: str,
    title: str
) -> str:
    """
    Generate chart with caching

    Note: data_hash should be a hash of the data to enable caching
    """
    # Regenerate data from hash (or use external cache)
    # This is simplified - in practice, use Redis or similar
    return generate_bar_chart(data, title)

def hash_chart_data(data: List[Dict]) -> str:
    """Create hash of chart data for caching"""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()
```

### 4. Cleanup Old Images

```python
# cleanup_service.py
async def cleanup_unused_images(
    sheet_id: str,
    storage: ImageStorageService
):
    """
    Remove images from storage that are no longer referenced
    """
    # 1. Get all image URLs in sheet
    sheet = await sheet_server.get_sheet_by_id(sheet_id)
    referenced_urls = set()

    for resource in sheet.resources:
        if resource.name == "SHEET_DRAWING_PLUGIN":
            drawing_data = json.loads(resource.data)
            for sheet_drawings in drawing_data.values():
                for drawing in sheet_drawings.values():
                    if drawing.get("imageSourceType") == "URL":
                        referenced_urls.add(drawing["source"])

    # 2. Get all images in storage for this sheet
    # (Implementation depends on your storage system)
    all_images = await storage.list_images(prefix=f"sheet-{sheet_id}")

    # 3. Delete unreferenced images
    for image_url in all_images:
        if image_url not in referenced_urls:
            await storage.delete_image(image_url)
```

---

## Summary & Recommendations

| Feature | Implementation | When to Use |
|---------|---------------|-------------|
| **Images** | ✅ Native support | Always available |
| **Charts** | Generate as images (matplotlib/plotly) | OSS version |
| **Storage: Base64** | Embed in MongoDB | Small images (<100KB) |
| **Storage: URL** | S3/CDN + MongoDB reference | Large images, production |
| **MCP Integration** | Backend API wrapper | Workflow automation |

### Recommended Architecture

```
Workflow/MCP Tool
    ↓
Generate Chart (matplotlib)
    ↓
Convert to PNG/Base64
    ↓
Python API
    ↓
Decision: Size < 100KB?
    ↓                    ↓
   YES                  NO
    ↓                    ↓
Store Base64         Upload to S3
in MongoDB          Store URL in MongoDB
    ↓                    ↓
    └────────┬───────────┘
             ↓
    Frontend loads sheet
             ↓
    Univer displays image
```

### Key Takeaways

1. ✅ **Images fully supported** in Univer OSS
2. ⚠️ **Charts** require generation as images (not native in OSS)
3. 💾 **Storage**: Use base64 for small, S3+URL for large
4. 🔧 **MCP Tools**: Easy to integrate via backend API
5. 📊 **Chart libraries**: matplotlib (simple) or plotly (interactive)

---

## References

- [Univer Drawing Package](https://github.com/dream-num/univer/tree/main/packages/drawing)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Plotly Python](https://plotly.com/python/)
- [AWS S3 SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
