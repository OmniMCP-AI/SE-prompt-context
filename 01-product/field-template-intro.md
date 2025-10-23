
## 🧩 What Is a “Field Template” in a Sheet-like Product

A **field template** defines the structure, behavior, and logic of a column (field) in a spreadsheet-style app such as Airtable, Notion tables, SmartSuite, or AI Sheets.
It’s the **blueprint for data consistency** — determining what type of data goes into a field, how it behaves, and how it integrates with automation or AI.

---

### 💡 **Core Idea**

Each field (or column) is not just a container of data, but a **typed object** with predefined rules and behavior.
A field template defines:

* Data type (text, number, date, etc.)
* Validation rules (required, unique, regex pattern)
* Formatting (currency symbol, precision, date format)
* Relationships (link to another record, formula field)
* Optional AI logic (auto-categorize, summarize, extract entities)

---

### 📘 **Example: Product Table**

| Product Name | Price | Launch Date | Category   | Status   |
| ------------ | ----- | ----------- | ---------- | -------- |
| iPhone 16    | $999  | 2025-09-20  | Smartphone | ✅ Active |

| Field        | Field Template Type | Description                                   |
| ------------ | ------------------- | --------------------------------------------- |
| Product Name | Text                | Free-form text (required)                     |
| Price        | Currency            | Only numbers, formatted as currency           |
| Launch Date  | Date                | Date picker with YYYY-MM-DD format            |
| Category     | Single Select       | Predefined list: Smartphone / Laptop / Tablet |
| Status       | Checkbox / Boolean  | Shows ✅ when true                             |

---

## 🧠 **User-Defined Field Templates**

Beyond built-in field types, users can **define their own field templates** to fit unique business or workflow needs.

### 🔧 **How They Work**

A user-defined field template allows you to:

* Create **custom data logic** once, then reuse it across many tables
* Combine **data type + formatting + logic + AI** into a reusable definition
* Share and apply templates across teams or databases

---

### 🧱 **Examples of User-Defined Field Templates**

| Template Name             | Base Type      | Custom Logic                                         | Example Use Case                           |
| ------------------------- | -------------- | ---------------------------------------------------- | ------------------------------------------ |
| **SKU Code**              | Text           | Auto-generate from `{Category}-{ID}`                 | Automatically creates SKU for each product |
| **Profit Margin**         | Formula        | `(Sale Price - Cost) / Sale Price`                   | Calculates margin percentage               |
| **AI Product Summary**    | AI Text        | Summarize `Product Description` into <100 words      | Auto-generate marketing blurbs             |
| **Status Tracker**        | Select         | Options = ["Draft", "In Review", "Published"]        | Used for content or product lifecycle      |
| **Region-Specific Price** | Computed Field | Fetch exchange rate from API, multiply by base price | Localizes price dynamically                |

---

### ⚙️ **Why User-Defined Templates Matter**

* 🔁 **Reusability:** Avoid repeating setup for common fields (like “Price”, “Owner”, or “Category”)
* ✅ **Consistency:** Standardize data structures across projects or teams
* 🤖 **Automation-ready:** Make it easier to integrate workflows (n8n, Zapier, etc.)
* 🧩 **Scalability:** Teams can publish shared template libraries — like “Marketing Fields”, “CRM Fields”, or “Finance Fields”

---

### 🧭 **Analogy**

Think of **built-in field templates** as “core data types” (like `string`, `number`, `boolean`)
and **user-defined field templates** as “custom classes” — they inherit basic behavior but add domain-specific intelligence.

---