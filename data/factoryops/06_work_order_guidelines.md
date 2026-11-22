# FactoryOps — Work Order Guidelines

## 1. Purpose

This document describes the Work Order Management module in FactoryOps.

Work orders are used to organize, assign, execute, and track maintenance and repair activities across factory machines.

The module supports:

- Work-order creation
- Incident escalation
- Machine and production references
- Work-order priority management
- Technician assignment
- Repair execution tracking
- Spare-parts linkage
- Work-order completion
- Cost and downtime tracking

The RAG assistant should use this document to explain work-order processes and retrieve current work-order information from the operational database.

---

## 2. Work Order Overview

| Property | Details |
|---|---|
| Factory | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Factory Code | APX-01 |
| Production Lines | L01–L04 |
| Core Machines | M001–M024 |
| Database Table | `work_orders` |
| Frontend Page | `WorkOrdersPage.tsx` |
| Backend | Node.js + Express + TypeScript |

Work orders are part of the FactoryOps maintenance and incident-management workflows.

A work order can be created independently or generated through incident escalation.

---

## 3. Work Order Identifiers

Work orders use identifiers in the following format:

`WO-2026-XXXX`

Example:

`WO-2026-0001`

Each work order has a unique `work_order_id`.

The assistant should use the actual identifier retrieved from the database when discussing a specific work order.

Never invent work-order identifiers.

---

## 4. Work Order Database Structure

The primary database table is:

`work_orders`

Important columns in the inspected SQL schema include:

| Column | Description |
|---|---|
| id | Internal primary key |
| work_order_id | Unique work-order identifier |
| maintenance_id | Associated maintenance record |
| incident_id | Associated incident |
| production_id | Associated production record |
| factory_id | Factory identifier |
| machine_id | Machine identifier |
| machine_name | Machine name |
| line_id | Production line identifier |
| line_name | Production line name |
| station_number | Station number |
| work_order_type | Work-order category |
| title | Work-order title |
| problem_description | Description of the issue |
| priority | Work-order priority |
| status | Current work-order status |
| assigned_to | Assigned user |
| technician_id | Technician identifier |
| technician_name | Technician name |
| due_date | Work-order due date |
| created_at | Creation timestamp |
| creation_timestamp | Recorded creation timestamp |
| start_time | Work start time |
| end_time | Work end time |
| completed_at | Completion timestamp |
| estimated_hours | Estimated work duration |
| actual_hours | Actual work duration |
| duration_minutes | Recorded duration |
| downtime_minutes | Recorded downtime |
| labor_hours | Labor hours |
| labor_cost | Labor cost |
| parts_cost | Spare-parts cost |
| total_cost | Total work-order cost |
| parts_required | Required spare parts |
| parts_replaced | Replaced spare parts |
| root_cause | Identified root cause |
| action_taken | Corrective action |
| service_provider | Service provider information |

### Schema difference

The application code also writes a `failure_category` field, but it is missing from the inspected `supabase-schema.sql` CREATE TABLE definition.

The actual deployed database schema must be verified before querying this field.

---

## 5. Work Order Types

FactoryOps contains seven work-order types in the supplied dataset.

| Work Order Type | General Purpose |
|---|---|
| Corrective | Corrective maintenance activities. |
| Changeover Alignment | Alignment activities during changeovers. |
| Preventive | Planned preventive maintenance. |
| Inspection | Equipment inspection activities. |
| Calibration | Calibration activities. |
| Breakdown | Work associated with equipment breakdowns. |
| Predictive | Predictive maintenance activities. |

These categories describe the work-order classification.

The assistant must not assume that every work-order type has a dedicated automated workflow.

---

## 6. Work Order Priorities

FactoryOps supports four priority levels.

| Priority | General Meaning |
|---|---|
| Low | Lower-priority work. |
| Medium | Normal operational priority. |
| High | Higher-priority work. |
| Critical | Critical work requiring urgent attention. |

The inspected database schema defines `Medium` as the default priority.

The application uses priority information to organize and display work orders.

### Important limitation

Official response-time targets, completion deadlines, and cost-based approval thresholds have not been established in the inspected application documentation.

Do not invent priority-based SLAs.

---

## 7. Work Order Status Lifecycle

### Application statuses

The application UI and backend support these statuses:

| Status | General Meaning |
|---|---|
| Pending | Work order is awaiting further action. |
| Open | Work order is open. |
| Scheduled | Work is scheduled. |
| Assigned | Work has been assigned. |
| In Progress | Work is being executed. |
| Pending Parts | Work is waiting for required parts. |
| On Hold | Work is temporarily paused. |
| Completed | Work has been completed. |
| Cancelled | Work order has been cancelled. |

### Dataset statuses

The supplied cleaned dataset contains 129 work-order records with these observed statuses:

- Completed
- In Progress
- Scheduled
- Open
- Pending Parts

The dataset does not contain every status supported by the application.

The assistant must distinguish between statuses observed in the dataset and statuses supported by the application.

---

## 8. Work Order Creation

Only the following roles can create work orders:

- ADMIN
- SUPER_ADMIN
- MANAGER_SUPERVISOR

The backend endpoint is:

`POST /api/work-orders`

### Creation process

1. An authorized user opens the Work Orders page.
2. The user opens the work-order creation form.
3. The user selects or provides relevant machine information.
4. The user enters the work-order title and problem description.
5. The user selects the work-order type.
6. The user selects a priority.
7. The user may provide assignment and scheduling information.
8. The user may associate an incident or other operational record.
9. The backend validates the request and creates the work order.

Work orders can be created independently or through incident escalation.

### Permission restrictions

The backend rejects work-order creation attempts from:

- TECHNICIAN
- PRODUCTION_PLANNER

These attempts receive HTTP 403.

A frontend button being visible does not override backend authorization.

---

## 9. Incident-to-Work-Order Escalation

Managers and administrators can escalate an incident by creating a work order.

The incident information can be prefilled in the work-order creation form.

This includes:

- Incident ID
- Machine ID
- Incident title
- Mapped priority

### Incident severity mapping

| Incident Severity | Work Order Priority |
|---|---|
| Critical | Critical |
| High | High |
| Medium | Medium |
| Low | Medium |

The work order can then be managed independently through its lifecycle.

The assistant must not assume that every incident automatically creates a work order.

---

## 10. Work Order Execution

Technicians can update the status of work orders assigned to them.

Examples of permitted task updates include:

- In Progress
- Pending Parts

The backend endpoint is:

`PATCH /api/work-orders/:id`

The backend enforces technician restrictions.

### Technician completion restriction

A technician cannot directly transition a work order to:

`Completed`

An attempt to do so returns HTTP 403.

Completion requires an authorized manager or administrator action, or the verified technician assignment closure workflow.

This is an important segregation-of-duties rule.

---

## 11. Work Order Completion and Sign-Off

Work orders can be completed through two supported paths.

### Path A: Authorized Manager or Administrator

The following roles can complete a work order through the backend update endpoint:

- ADMIN
- SUPER_ADMIN
- MANAGER_SUPERVISOR

### Path B: Verified Technician Assignment

When a manager verifies a technician's completed repair through the Technician Assignment workflow, the linked work order is automatically updated.

The verification endpoint is:

`POST /api/technician-assignments/:id/verify`

This process also synchronizes the linked incident record.

### Important rule

Technician repair execution and final work-order completion are separate responsibilities.

The assistant must never tell a technician that they can independently approve and complete their own assigned work order.

---

## 12. Work Order Deletion

The following roles can delete work orders:

- ADMIN
- SUPER_ADMIN
- MANAGER_SUPERVISOR

The backend endpoint is:

`DELETE /api/work-orders/:id`

Technicians and Production Planners do not have permission to delete work orders.

Deletion should never be recommended as a substitute for changing a work-order status.

---

## 13. Spare Parts Linkage

Work-order creation supports optional spare-parts selection.

The application retrieves available inventory information through:

`/api/inventory`

Selected spare parts are stored as text in the work order's:

`parts_required`

### Important implementation limitation

Selecting spare parts for a work order does not automatically decrease inventory stock.

The assistant must not claim that inventory quantities are automatically deducted when a work order is created.

Current stock quantities must be retrieved from the inventory data.

The relationship between work orders and inventory should be verified against actual records before reporting parts usage.

---

## 14. Work Order Costs and Duration

Work orders contain fields related to time and financial tracking.

### Time-related fields

- `estimated_hours`
- `actual_hours`
- `duration_minutes`
- `downtime_minutes`
- `labor_hours`
- `start_time`
- `end_time`

### Cost-related fields

- `labor_cost`
- `parts_cost`
- `total_cost`

These fields support operational analysis.

Possible metrics include:

- Estimated versus actual hours
- Total recorded labor hours
- Total recorded downtime
- Labor cost
- Spare-parts cost
- Total work-order cost

### Currency limitation

The currency used in the supplied maintenance and work-order datasets has not been verified.

The UI formatting displays a dollar symbol for cost values, but this does not establish the actual currency.

The assistant must not automatically label work-order costs as INR or USD.

Until the currency is confirmed, report the recorded numeric values with a clear currency limitation.

---

## 15. Work Order Data Quality

The supplied cleaned work-order dataset contains:

| Attribute | Observed Value |
|---|---|
| Total records | 129 |
| Date range | 2026-07-01 to 2026-10-03 |
| Work-order ID pattern | WO-2026-XXXX |
| Work-order types | 7 |
| Priority levels | 4 |

### Missing relationship references

The dataset contains these placeholder values:

| Field | Placeholder Count |
|---|---:|
| maintenance_id | 43 |
| incident_id | 43 |
| production_id | 41 |

The literal value `Not Linked` represents an unavailable relationship.

It must be treated as NULL for database joins and analytical calculations.

### Invalid sentinel values

The supplied dataset contains:

- 2 `downtime_minutes` values equal to `-1`.
- 2 `labor_hours` values equal to `-1`.

These are sentinel values, not actual negative measurements.

The RAG assistant must exclude them or treat them as NULL when calculating totals and averages.

### Currency ambiguity

Work-order cost values have not been assigned a verified currency standard.

Do not generate financial reports that imply an unconfirmed currency.

---

## 16. Work Order Analytics

FactoryOps supports the following work-order metrics.

### Total Work Orders

The total number of work-order records.

### Open and Pending Queue

The number of work orders awaiting action.

The exact status filters must be defined according to the application's reporting logic.

### Status Breakdown

Work-order counts grouped by status.

### Priority and Status Distribution

Work orders grouped by both priority and status.

### Technician Workload

Work orders grouped by assigned technician.

Access to technician-level information must respect role permissions.

### Estimated versus Actual Hours

Comparison of estimated and actual work duration.

### Work Order Costs

Analysis of:

- Labor cost
- Parts cost
- Total cost

Currency must be confirmed before presenting formatted financial values.

All live counts and calculations must come from structured operational database queries.

---

## 17. Role-Based Work Order Responsibilities

| Role | Work Order Responsibilities |
|---|---|
| SUPER_ADMIN | Authorized work-order creation, updates, completion, and deletion. |
| ADMIN | Authorized work-order creation, updates, completion, and deletion. |
| MANAGER_SUPERVISOR | Authorized work-order creation, updates, completion, and deletion. |
| PRODUCTION_PLANNER | Work-order visibility according to assigned permissions; cannot create work orders. |
| TECHNICIAN | Update assigned work tasks; cannot create, delete, or directly complete work orders. |

Actual access must be enforced by backend authorization.

The assistant must not use frontend button visibility as proof of permission.

---

## 18. RAG Retrieval Guidelines

The RAG assistant should classify work-order questions into three categories.

### Knowledge-based questions

Examples:

- What are the work-order priority levels?
- What are the available work-order statuses?
- Who can create work orders?
- Can technicians complete work orders?
- How are incidents escalated into work orders?
- Does selecting spare parts automatically update inventory?

Use this document to answer.

### Operational questions

Examples:

- How many work orders are currently open?
- Show all critical work orders.
- Which technician has the most assigned work?
- What is the status of WO-2026-0001?
- What is the total recorded work-order downtime?

Use structured database queries against `work_orders`.

### Hybrid questions

Examples:

- Explain work-order escalation and show how many incident-linked work orders are open.
- Explain technician completion restrictions and show the current pending work orders.
- Explain spare-parts linkage and identify work orders with recorded parts requirements.

Use this document for explanations and structured database queries for current information.

---

## 19. Accuracy and Security Rules

The RAG assistant must follow these rules:

1. Never invent work-order identifiers.
2. Never assume that every incident has a linked work order.
3. Never treat `Not Linked` as a valid database identifier.
4. Treat `-1` downtime and labor values as missing data.
5. Never allow technicians to directly complete work orders.
6. Never allow unauthorized roles to create or delete work orders.
7. Do not claim that spare-parts selection automatically decreases inventory stock.
8. Do not assume that work-order completion automatically creates a maintenance record.
9. Do not assume that all work-order types have automated workflows.
10. Do not invent official SLAs or approval thresholds.
11. Do not assume the currency of cost fields.
12. Verify schema-drift fields before using them in database queries.
13. Use live operational queries for current work-order counts and statuses.
14. Enforce backend role-based access control.

---

## 20. Pending Business Decisions

The following items require confirmation from authorized stakeholders:

- Official work-order response-time SLAs.
- Official completion-time SLAs.
- Priority-based escalation timelines.
- Cost approval thresholds.
- Verified currency standard.
- Formal work-order closure policy beyond the implemented workflows.

Until confirmed, the assistant must not present these as official FactoryOps policies.

---

## 21. Summary

FactoryOps Work Order Management provides a structured process for creating, prioritizing, assigning, executing, and completing maintenance and repair tasks.

Work orders can be linked to incidents, machines, production records, and spare-parts information.

Managers and administrators control work-order creation and completion, while technicians can update assigned tasks but cannot independently complete work orders.

The RAG assistant should use this document for workflow explanations and structured database queries for live work-order information.