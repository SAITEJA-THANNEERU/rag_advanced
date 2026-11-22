# FactoryOps — Inventory and Spare Parts Management

## 1. Purpose

FactoryOps includes a Spare Parts Inventory module to manage spare parts required for machine maintenance and repair activities.

The inventory module supports:

- Spare parts catalog management.
- Stock quantity monitoring.
- Category-based filtering.
- Supplier information.
- Inventory cost tracking.
- Low-stock identification.
- Quick restocking.
- Spare parts selection during work-order creation.

The module helps factory teams monitor spare-part availability and identify items that require replenishment.

---

## 2. Inventory Module Overview

**Frontend:** `src/pages/InventoryPage.tsx`

**Backend endpoints:**

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/inventory` | Retrieve inventory records. |
| POST | `/api/inventory` | Create an inventory item. |
| PUT | `/api/inventory/:id` | Update an inventory item. |
| DELETE | `/api/inventory/:id` | Delete an inventory item. |

The module provides a catalog interface with inventory information and stock-management controls.

---

## 3. Inventory Information

The inventory module supports information related to:

- Spare part identification.
- SKU/catalog information.
- Part category.
- Supplier.
- Unit cost.
- Available stock quantity.
- Minimum reorder level.
- Storage or bin location, where recorded.

**Data limitation:** The inspected source confirms these inventory capabilities, but the complete live `spare_parts` database schema and every field definition were not available for verification.

Do not assume that every field above has a confirmed database column.

---

## 4. Spare Parts Categories

The inventory interface supports category-based filtering.

Users can organize and search inventory items using the available category information.

The inspected analysis does not establish a complete authoritative list of spare-part categories.

Therefore, the RAG assistant must retrieve category names from actual inventory records rather than inventing a fixed category list.

---

## 5. Stock Quantity and Reorder Level

FactoryOps uses the following low-stock rule:

```text
stock_quantity <= min_reorder_level
```

An inventory item is considered low-stock when its available quantity is less than or equal to its minimum reorder level.

### Example

| Part | Stock Quantity | Minimum Reorder Level | Result |
|---|---:|---:|---|
| SP-001 | 20 | 10 | Normal |
| SP-002 | 10 | 10 | Low Stock |
| SP-003 | 5 | 10 | Low Stock |
| SP-004 | 0 | 10 | Low Stock |

These values are illustrative examples, not actual FactoryOps inventory records.

### Low-stock behavior

When an item reaches or falls below its minimum reorder level:

- The inventory interface displays a critical low-stock warning.
- The item receives a low-stock badge.
- Users can identify the item for replenishment.

---

## 6. Inventory Restocking

FactoryOps supports quick restocking through the inventory interface.

Authorized users can increase stock quantities through the available inventory functionality.

The inventory module supports restocking as part of stock management.

### Important distinction

Restocking is an inventory operation.

Selecting a spare part for a work order does not automatically mean that inventory has been replenished or consumed.

The application must distinguish between:

- Available inventory.
- Inventory restocking.
- Parts requested for a work order.
- Parts actually replaced during maintenance.

---

## 7. Supplier Information

The inventory interface supports supplier-related information and supplier-based filtering.

Supplier information can help users identify where spare parts are sourced.

The inspected source does not establish:

- An authoritative supplier directory.
- Supplier approval procedures.
- Purchase-order workflows.
- Supplier delivery SLAs.
- Automatic supplier notifications.

The RAG assistant must retrieve supplier details from actual inventory records.

It must not invent supplier names, contact information, or delivery timelines.

---

## 8. Spare Parts and Work Orders

FactoryOps allows users to select spare parts from the inventory catalog while creating a work order.

### Work-order integration

During work-order creation:

1. The user opens the work-order creation interface.
2. Available inventory items can be retrieved through `/api/inventory`.
3. The user selects the required spare parts.
4. The selected information is inserted into the work order's `parts_required` field.

### Important limitation

The current implementation stores selected spare-part information as text in `parts_required`.

Selecting a part for a work order does not automatically:

- Decrease inventory stock.
- Create a stock reservation.
- Record an inventory consumption transaction.
- Confirm that the part was physically used.
- Update inventory after work-order completion.

The assistant must not claim that inventory has been automatically deducted when a part is added to a work order.

---

## 9. Work-Order Parts Fields

The verified `work_orders` schema includes:

| Field | Purpose |
|---|---|
| `parts_required` | Spare parts required for the work order. |
| `parts_replaced` | Spare parts recorded as replaced. |
| `parts_cost` | Parts-related cost. |
| `total_cost` | Total work-order cost. |

The fields support maintenance and work-order reporting.

The currency unit for maintenance and work-order costs has not been conclusively verified.

Do not assume whether these values represent INR or USD.

---

## 10. Role-Based Inventory Permissions

FactoryOps uses role-based access control for inventory operations.

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View inventory | Yes | Yes | Yes | Yes | Yes |
| Create inventory items | Yes | Yes | Yes | No | No |
| Edit inventory items | Yes | Yes | Yes | No | Yes |
| Restock inventory | Yes | Yes | Yes | No | Yes |
| Delete inventory items | Yes | Yes | Yes | No | No |

### SUPER_ADMIN

Can manage inventory records and restocking.

### ADMIN

Can manage inventory records and restocking.

### MANAGER_SUPERVISOR

Can manage inventory records and restocking.

### PRODUCTION_PLANNER

Has read-only inventory access.

### TECHNICIAN

Can:

- View inventory.
- Edit permitted inventory information.
- Restock inventory.

Cannot delete inventory items.

### RAG authorization requirement

The assistant must enforce the authenticated user's inventory permissions.

It must not offer unauthorized inventory creation, editing, restocking, or deletion actions.

---

## 11. Inventory Analytics

The inventory module can support operational questions such as:

- How many spare parts are available?
- Which parts are low-stock?
- Which items have zero available stock?
- Which parts belong to a particular category?
- Which supplier is associated with a particular item?
- What is the current stock quantity of a specific SKU?
- Which parts may be required for a work order?

These questions should use current structured inventory records.

The RAG vector database should not be treated as the authoritative source for live stock quantities.

---

## 12. Recommended RAG Integration

Inventory questions usually require structured database retrieval rather than document-only vector search.

Recommended read-only operational tool:

```text
getSparePartsStock(
    lowStockOnly?,
    category?,
    search?
)
```

### Example query

User:

"Show all low-stock spare parts."

Expected behavior:

1. Authenticate the user.
2. Verify inventory-view permission.
3. Retrieve current inventory records.
4. Apply the condition:

   `stock_quantity <= min_reorder_level`

5. Return matching parts.
6. Include SKU, available quantity, reorder level, and supplier information when available.

### Example query

User:

"Is spare part SP-001 available?"

Expected behavior:

1. Search the current inventory records.
2. Retrieve the matching SKU.
3. Return the actual stock quantity.
4. Compare it with the minimum reorder level.
5. Explain whether it meets the application's low-stock condition.

The assistant must not rely on outdated vector embeddings for current inventory quantities.

---

## 13. Important Data and Implementation Limitations

The following limitations must be considered during RAG integration:

1. The complete `spare_parts` SQL table definition was not available in the inspected schema files.
2. The live Supabase inventory schema has not been independently verified.
3. The current work-order parts linkage uses text storage.
4. Selecting parts for a work order does not automatically decrement inventory.
5. A complete purchase-order and procurement workflow was not verified.
6. A complete supplier directory and supplier approval process were not verified.
7. Automatic stock reservation and consumption tracking were not verified.

These limitations must be communicated accurately.

---

## 14. RAG Accuracy Rules

The FactoryOps RAG assistant must follow these rules:

1. Use actual inventory records for current stock information.
2. Apply the exact low-stock condition: `stock_quantity <= min_reorder_level`.
3. Do not invent SKUs, suppliers, categories, or stock quantities.
4. Respect role-based inventory permissions.
5. Do not claim that work-order part selection automatically reduces stock.
6. Distinguish required parts from replaced parts.
7. Do not assume a currency unit for inventory or maintenance costs.
8. Clearly state when inventory information is unavailable.
9. Use structured queries for stock counts and live availability.
10. Never allow the LLM to execute unrestricted database queries.

---

## 15. Summary

FactoryOps provides a Spare Parts Inventory module for catalog management, stock monitoring, supplier information, low-stock warnings, and restocking.

Its low-stock condition is:

`stock_quantity <= min_reorder_level`

Spare parts can be selected while creating work orders, but the current implementation stores the selection in `parts_required` without automatically reducing inventory quantities.

For the Advanced RAG integration, live inventory questions should use authenticated, role-restricted structured database queries.

The assistant must distinguish actual inventory stock from parts requested or recorded in work orders.