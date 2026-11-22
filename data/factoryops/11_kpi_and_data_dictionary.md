# FactoryOps — KPI and Data Dictionary

## 1. Purpose

This document defines the operational database structure, important data fields, dataset mappings, KPI calculations, and known data-quality issues in FactoryOps.

It is particularly important for the Advanced RAG integration because the assistant must answer questions involving:

- Machine performance.
- Production output.
- Defects and scrap.
- Maintenance history.
- Incident statistics.
- Work-order status.
- Inventory availability.
- Operational costs.
- Overall Equipment Effectiveness (OEE).

The assistant must use actual structured database queries for live operational numbers rather than relying only on vector search.

---

# 2. FactoryOps Database Overview

FactoryOps uses Supabase PostgreSQL as its cloud database, with an application-level persistence fallback.

The following database tables were identified from the inspected SQL files and backend implementation.

## 2.1 Verified Database Tables

| No. | Table | Category | SQL Columns | Status |
|---|---|---|---:|---|
| 1 | `factories` | Operational / Tenant | 11 | Verified |
| 2 | `machines` | Operational | 29 | Verified |
| 3 | `production_records` | Operational | 29 | Schema drift |
| 4 | `maintenance_records` | Operational | 32 | Schema drift |
| 5 | `incidents` | Operational | 30 | Verified |
| 6 | `work_orders` | Operational | 38 | Schema drift |
| 7 | `sops` | Operational / Knowledge | 12 | Verified |
| 8 | `data_quality_metrics` | Operational / IoT | 10 | Verified |
| 9 | `users` | User / Identity | 10 | Verified |
| 10 | `notifications` | User / Workflow | 15 | Verified |
| 11 | `technician_profiles` | Workforce | 22 | Verified |
| 12 | `technician_incident_assignments` | Operational / Workflow | 42 | Verified |
| 13 | `repair_progress_updates` | Operational / Workflow | Not specified | Verified |
| 14 | `reassignment_requests` | Operational / Workflow | Not specified | Verified |
| 15 | `incident_resolution_submissions` | Operational / Workflow | Not specified | Verified |
| 16 | `incident_verification_details` | Operational / Workflow | Not specified | Verified |

### Additional tables with incomplete database definitions

| Table | Current Finding |
|---|---|
| `spare_parts` | Referenced by backend and RLS configuration; CREATE TABLE definition missing from inspected SQL files. |
| `system_audit_logs` | Referenced by backend and RLS configuration; CREATE TABLE definition missing from inspected SQL files. |
| `attendance_records` | Referenced in RLS configuration; CREATE TABLE definition missing and not synced by inspected backend synchronization code. |
| `factory_locations` | Local JSON/in-memory persistence; no inspected SQL definition. |
| `attendance_audit_logs` | Local JSON/in-memory persistence; no inspected SQL definition. |

**Important:** These findings describe the inspected repository SQL and application code. The actual deployed Supabase schema has not been independently inspected.

---

# 3. Primary Operational Tables

## 3.1 Factories

Table:

`factories`

Purpose:

Stores factory-level information.

Primary key:

`id`

Unique field:

`factory_code`

Foreign-key relationships from operational tables generally reference:

`factories(id)`

Current active factory:

| Field | Value |
|---|---|
| Factory ID | FAC-001 |
| Factory Code | APX-01 |
| Factory Name | Apex Precision Manufacturing |
| Location | Hyderabad, Telangana |

The application currently operates in single-factory mode for FAC-001.

---

## 3.2 Machines

Table:

`machines`

Purpose:

Stores factory machine information, technical specifications, and machine status.

Important fields identified in the application include:

| Field | Purpose |
|---|---|
| `id` | Primary key. |
| `machine_id` | Machine identifier, such as M001. |
| `factory_id` | Factory reference. |
| `name` / `machine_name` | Machine name. |
| `line_id` | Production line identifier. |
| `line_name` | Production line name. |
| `station_number` | Station information. |
| `status` | Machine operational status. |
| `temperature` | Displayed temperature. |
| `vibration` | Displayed vibration. |
| `speed` | Displayed speed. |
| `pressure` | Displayed pressure. |
| `oee` | Machine OEE value. |
| `health_score` | Machine health score. |

### Machine identifiers

The core machine registry uses:

`M001` through `M024`.

### Important relationship limitation

Operational records are linked to machines using text-based `machine_id` values.

The inspected schema does not establish foreign-key constraints for every machine-related operational relationship.

The assistant should use validated machine identifiers when joining records.

---

## 3.3 Production Records

Table:

`production_records`

Purpose:

Stores machine production information by shift and date.

### Verified SQL columns

The inspected SQL schema includes:

- `id`
- `production_id`
- `factory_id`
- `machine_id`
- `machine_name`
- `timestamp`
- `date`
- `shift`
- `line_id`
- `line_name`
- `station_number`
- `product_id`
- `product_name`
- `target_units`
- `planned_units`
- `actual_units`
- `defective_units`
- `defect_units`
- `scrap_kg`
- `downtime_minutes`
- `speed_rpm`
- `temperature_c`
- `vibration_mms`
- `cycle_time_sec`
- `operator`
- `operator_id`
- `operator_name`
- `remarks`

### Additional fields used by application code and CSV

The following fields are also used:

- `good_units`
- `planned_downtime_minutes`
- `unplanned_downtime_minutes`
- `target_cycle_time_seconds`
- `actual_cycle_time_seconds`
- `availability_percent`
- `performance_percent`
- `quality_percent`
- `oee_percent`
- `changeover_minutes`
- `status`

These additional fields are absent from the inspected `supabase-schema.sql` CREATE TABLE definition.

This is a schema-drift issue that must be reconciled before production RAG database queries are finalized.

---

## 3.4 Maintenance Records

Table:

`maintenance_records`

Purpose:

Stores maintenance activities performed on factory machines.

### Verified SQL fields

Important columns include:

- `id`
- `maintenance_id`
- `factory_id`
- `machine_id`
- `machine_name`
- `line_id`
- `line_name`
- `station_number`
- `type`
- `maintenance_type`
- `status`
- `failure_category`
- `scheduled_date`
- `completed_date`
- `start_time`
- `end_time`
- `downtime_minutes`
- `downtime_hours`
- `logged_timestamp`
- `calculated_duration`
- `technician`
- `technician_id`
- `technician_name`
- `description`
- `problem_description`
- `action_taken`
- `parts_replaced`
- `parts_cost`
- `labor_cost`
- `cost_usd`
- `total_cost`

### Additional fields used by application code and CSV

- `priority`
- `root_cause`
- `duration_minutes`
- `labor_hours`
- `work_order_id`
- `service_provider`
- `sign_off_by`
- `remarks`

These fields are mapped by the application but are missing from the inspected SQL CREATE TABLE definition.

### Data limitations

The maintenance dataset contains 210 records.

All 210 records have status `Completed`.

The technician IDs in the dataset use T01–T08, which do not match the application's technician profile identifiers.

Cost currency also requires confirmation.

---

## 3.5 Incidents

Table:

`incidents`

Purpose:

Stores operational incidents reported against machines and production processes.

Important fields include:

- `id`
- `incident_id`
- `factory_id`
- `machine_id`
- `machine_name`
- `line_id`
- `line_name`
- `station_number`
- `title`
- `description`
- `severity`
- `status`
- `failure_category`
- `production_id`
- `maintenance_id`
- `work_order_id`
- `downtime_minutes`
- `defect_units`
- `root_cause`
- `action_taken`
- `resolution_notes`
- `resolved_at`
- `reported_by`
- `created_at`

The exact deployed schema must be checked before implementing live queries.

### Incident categories

- Sensor/Optical
- Mechanical
- Tooling
- Hydraulic
- Electrical
- Chemical
- Thermal/Cooling
- Pneumatic

### Severity levels

- Low
- Medium
- High
- Critical

### Dataset profile

109 incident records were identified.

Date range:

2026-07-01 to 2026-09-08.

---

## 3.6 Work Orders

Table:

`work_orders`

Purpose:

Stores maintenance and operational work orders.

### Verified SQL fields

The inspected SQL schema includes:

- `id`
- `work_order_id`
- `maintenance_id`
- `incident_id`
- `production_id`
- `factory_id`
- `machine_id`
- `machine_name`
- `line_id`
- `line_name`
- `station_number`
- `work_order_type`
- `title`
- `problem_description`
- `priority`
- `status`
- `assigned_to`
- `technician_id`
- `technician_name`
- `due_date`
- `created_at`
- `creation_timestamp`
- `start_time`
- `end_time`
- `completed_at`
- `estimated_hours`
- `actual_hours`
- `duration_minutes`
- `downtime_minutes`
- `labor_hours`
- `labor_cost`
- `parts_cost`
- `total_cost`
- `parts_required`
- `parts_replaced`
- `root_cause`
- `action_taken`
- `service_provider`

### Schema drift

The application also writes `failure_category`, but it is absent from the inspected CREATE TABLE definition.

### Dataset profile

129 work-order records were identified.

Date range:

2026-07-01 to 2026-10-03.

### Work-order priorities

- Low
- Medium
- High
- Critical

---

## 3.7 SOPs

Table:

`sops`

Purpose:

Stores Standard Operating Procedures.

The inspected schema contains 12 columns.

Important fields include:

- `id`
- `sop_id`
- `factory_id`
- SOP title and descriptive information
- Version information
- `steps`
- `safety_precautions`

The `steps` and `safety_precautions` fields use PostgreSQL `TEXT[]`.

Four seeded SOPs are currently verified.

---

## 3.8 Data Quality Metrics

Table:

`data_quality_metrics`

Purpose:

Stores information displayed by the IoT Data Quality module.

The application currently displays four seeded sensor-health cards.

These should not be interpreted as proof of a live PLC/IoT ingestion pipeline.

---

# 4. User and Workflow Tables

| Table | Purpose |
|---|---|
| `users` | User identity, credentials, roles, and account status. |
| `notifications` | User notifications and event updates. |
| `technician_profiles` | Technician specialization and workforce profile. |
| `technician_incident_assignments` | Incident-to-technician assignment workflow. |
| `repair_progress_updates` | Technician repair progress history. |
| `reassignment_requests` | Technician reassignment requests. |
| `incident_resolution_submissions` | Submitted repair resolutions. |
| `incident_verification_details` | Repair verification information. |

### Authentication note

FactoryOps uses custom Express PBKDF2-SHA512 authentication.

It does not use Supabase Auth for its primary application login.

The backend issues session tokens and validates them through its authentication middleware.

The RAG service must integrate with the authenticated backend context rather than trusting a role supplied by the frontend.

---

# 5. Dataset Inventory

The following datasets were inspected in:

`/public/assets/aistudio/`

| Dataset | Rows | Columns | Date Range |
|---|---:|---:|---|
| Machine Data | 24 | 15 | Installation dates: 2021–2023 |
| Production Data | 6,480 | 23 | 2026-07-01 to 2026-09-28 |
| Maintenance Data | 210 | 28 | 2026-07-02 to 2026-10-02 |
| Incident Data | 109 | 25 | 2026-07-01 to 2026-09-08 |
| Work Order Data | 129 | 29 | 2026-07-01 to 2026-10-03 |

These counts describe the inspected CSV datasets, not guaranteed current live database totals.

---

# 6. Data Relationships

FactoryOps connects operational records using identifiers.

### Primary relationships

| Source | Related Record | Link Field |
|---|---|---|
| Production | Machine | `machine_id` |
| Maintenance | Machine | `machine_id` |
| Incident | Machine | `machine_id` |
| Work Order | Machine | `machine_id` |
| Incident | Production | `production_id` |
| Incident | Maintenance | `maintenance_id` |
| Work Order | Incident | `incident_id` |
| Work Order | Maintenance | `maintenance_id` |
| Work Order | Production | `production_id` |
| Technician Assignment | Incident | `incident_id` |
| Technician Assignment | Technician | `technician_id` |

### Important relationship limitation

Some relationships are text-based rather than enforced through SQL foreign keys.

The RAG analytical layer must validate identifiers and handle missing relationships safely.

---

# 7. Data Cleaning Rules

This section is especially important for accurate analytics.

## 7.1 The -1 Sentinel Value

The Work Order dataset contains `-1` values in:

| Column | Affected Rows |
|---|---:|
| `downtime_minutes` | 2 |
| `labor_hours` | 2 |

These values represent invalid or unavailable measurements in the inspected dataset.

They must not be treated as actual negative downtime or labor.

### Required handling

Convert these sentinel values to NULL or exclude them from numerical aggregation.

Example:

```sql
SELECT
    AVG(NULLIF(downtime_minutes, -1)) AS average_downtime
FROM work_orders;
```

The actual column type and deployed schema must be verified before using this exact query.

---

## 7.2 Not Linked Placeholders

The datasets contain the literal text:

`Not Linked`

Affected records:

| Dataset | Column | Rows |
|---|---|---:|
| Incident | `production_id` | 1 |
| Incident | `maintenance_id` | 41 |
| Work Order | `maintenance_id` | 43 |
| Work Order | `incident_id` | 43 |
| Work Order | `production_id` | 41 |

### Required handling

Normalize `Not Linked` to NULL before joining or performing relationship-based analysis.

Do not treat it as a valid production, maintenance, or incident identifier.

---

## 7.3 Technician Identifier Mismatch

Maintenance CSV records use technician identifiers:

`T01–T08`

The application uses identifiers such as:

`TECH-001–TECH-006`

and associated user IDs.

A verified mapping between these identifiers is not available.

The RAG assistant must not assume that similarly named technician IDs represent the same person.

---

## 7.4 Currency Ambiguity

Maintenance and work-order datasets contain cost information.

However, the currency unit has not been conclusively approved.

The application also uses a `cost_usd` field and UI formatting that displays dollar symbols.

This does not conclusively establish that all CSV costs are USD.

The assistant must not automatically convert or label these amounts as INR or USD.

---

# 8. Key Performance Indicators

FactoryOps displays several production and operational metrics.

The following formulas were identified in the inspected application.

## 8.1 Production Achievement

Measures actual production against planned production.

Formula:

```text
Production Achievement (%) =
(Sum of Actual Units / Sum of Planned Units) × 100
```

Example:

Planned production = 1,000 units.

Actual production = 900 units.

Achievement = 90%.

---

## 8.2 Production Shortfall

Measures the difference between planned and actual production.

Formula:

```text
Production Shortfall =
Sum of Planned Units - Sum of Actual Units
```

A negative value indicates production exceeded the plan.

---

## 8.3 Defect Rate

Formula:

```text
Defect Rate (%) =
(Sum of Defect Units / Sum of Actual Units) × 100
```

This is the machine-wise defect-rate calculation identified in the Admin Dashboard.

---

## 8.4 Yield Rate / First-Pass Yield

Formula:

```text
Yield Rate (%) =
((Actual Units - Defective Units) / Actual Units) × 100
```

The Quality page uses this calculation for yield-related reporting.

### Important limitation

The displayed Inspection Pass Rate of 99.4% is hardcoded.

It must not be presented as a dynamically calculated inspection metric.

---

## 8.5 Plant OEE

The backend plant OEE calculation uses machine-level OEE values.

Formula:

```text
Plant OEE =
Average OEE of eligible machines
```

Eligible machines exclude statuses:

- Offline
- Maintenance

If no eligible machine OEE values are available, the backend uses a fallback value of:

`85.0`

### Important limitation

This backend KPI uses machine-level OEE values.

It does not directly calculate plant OEE from all `production_records.oee_percent` values.

---

## 8.6 Production Record OEE

The production dataset includes:

- `availability_percent`
- `performance_percent`
- `quality_percent`
- `oee_percent`

These fields are available in the dataset and mapped by the application.

However, the canonical organization-wide OEE definition has not received final approval.

---

## 8.7 Availability

The backend KPI calculation uses a heuristic based on downtime.

The inspected implementation includes:

```text
Availability =
100 - (Total Downtime / Total Production Time × 100)
```

The result is subject to application-specific calculation logic and clamping.

The exact production-time denominator and its governance require confirmation before treating this as the official plant KPI.

---

## 8.8 Quality and Performance

The backend KPI calculation includes heuristic quality and performance calculations.

The inspected implementation includes:

```text
Quality =
Clamp(100 - Defect Rate, 90, 99.8)
```

Performance is back-calculated from OEE, Availability, and Quality:

```text
Performance =
Clamp(
    Average OEE / (Availability × Quality / 10000),
    80,
    99.0
)
```

These are backend KPI-generation formulas, not an approved universal manufacturing KPI standard.

---

# 9. Known KPI and Dashboard Discrepancies

The application contains differences between dashboard calculations.

| Metric | Discrepancy |
|---|---|
| Plant OEE | Backend uses machine-level OEE, while production records contain separate OEE values. |
| Admin Dashboard OEE | Averages all production OEE records, including zero values. |
| Manager Dashboard OEE | Averages all production OEE records, including zero values. |
| Super Admin OEE | Averages only records where OEE is greater than zero. |
| Inspection Pass Rate | Displays a hardcoded 99.4%. |
| Planner Machine Tooltip | Displays the sum of OEE values instead of the average in one tooltip. |
| Availability | Uses backend heuristic calculations. |
| Performance | Back-calculated from OEE, Availability, and Quality. |

### RAG instruction

The assistant must identify which KPI source it used.

It must not silently combine incompatible calculations.

For example, a query asking for plant OEE must identify whether it is reporting:

- Backend machine-level plant OEE.
- Production-record average OEE.
- A particular dashboard's OEE calculation.

Until KPI governance is approved, explain the calculation used.

---

# 10. Recommended Analytical Queries

The RAG integration should use parameterized read-only analytical functions rather than unrestricted LLM-generated SQL.

Recommended functions:

```text
getMachineStatusAndSpecs(
    machineId?,
    lineId?,
    status?
)
```

```text
queryProductionKPIs(
    machineId?,
    lineId?,
    shift?,
    dateFrom?,
    dateTo?
)
```

```text
queryIncidents(
    machineId?,
    severity?,
    status?,
    failureCategory?
)
```

```text
queryWorkOrders(
    machineId?,
    status?,
    priority?,
    assignedTo?
)
```

```text
queryMaintenanceHistory(
    machineId?,
    type?,
    dateFrom?,
    dateTo?
)
```

```text
getSparePartsStock(
    lowStockOnly?,
    category?,
    search?
)
```

```text
getTechnicianAssignmentsForCurrentUser()
```

The final function must enforce:

- Technician own-assignment restrictions.
- Production Planner redaction rules.
- Authenticated user identity.
- Factory-level access scope.

These functions should use validated inputs and approved database operations.

---

# 11. Database and Supabase Security Considerations

FactoryOps uses custom Express authentication, while its Supabase RLS configuration relies on Supabase JWT identity and claims.

This creates an architectural mismatch.

### Verified findings

- FactoryOps authentication uses custom PBKDF2-SHA512 credentials.
- Express maintains its own session tokens.
- Supabase RLS policies reference `auth.uid()` and JWT claims.
- Express requests do not automatically carry a Supabase Auth identity.
- Without the appropriate authenticated Supabase context, `auth.uid()` can be NULL.
- Using a service-role key bypasses normal RLS enforcement.

### Required architecture

The RAG backend must not expose a Supabase service-role key to the frontend.

If backend service-role access is used, the Express/RAG backend must enforce user identity, role permissions, and factory scoping before executing any query.

A final decision is required on how Supabase authentication and application-level authorization will work together.

---

# 12. RAG Knowledge Retrieval vs. Structured Database Retrieval

FactoryOps questions fall into three categories.

## 12.1 Knowledge Questions

Examples:

- What is the CNC operating procedure?
- What are the technician permissions?
- How does incident escalation work?
- What is the attendance geofence rule?

Use:

Vector retrieval and keyword search over the Markdown knowledge base.

## 12.2 Operational Analytics Questions

Examples:

- How many open incidents are there?
- What is the total production this month?
- Which machines have the highest downtime?
- Which spare parts are low-stock?

Use:

Authenticated, read-only structured database tools.

## 12.3 Hybrid Questions

Example:

"Machine M007 has high downtime. What incidents were reported and which safety SOP applies before servicing?"

Use:

1. Structured machine and downtime retrieval.
2. Incident-history retrieval.
3. SOP vector retrieval.
4. Role authorization.
5. Combined grounded response with citations.

A pure vector-RAG system cannot reliably answer live counts, sums, rankings, or changing operational statuses.

---

# 13. Recommended Data Ingestion and Indexing

For the unstructured FactoryOps knowledge documents, use:

- Markdown header-aware chunking.
- Approximately 400–600 tokens per chunk.
- Approximately 15% overlap.
- Preserve safety-critical steps and warnings together.

Recommended metadata:

```json
{
  "doc_id": "08_safety_procedures",
  "section_title": "CNC Machine Operating Procedure",
  "module": "safety",
  "machine_ids": [],
  "line_ids": [],
  "allowed_roles": [],
  "safety_critical": true,
  "verification_status": "VERIFIED",
  "version": "3.2",
  "updated_at": null
}
```

Use metadata filtering by:

- Factory ID.
- User role.
- Module.
- Machine ID.
- Line ID.
- Safety-critical status.
- Verification status.

For structured operational records, use database queries rather than embedding every production and maintenance row into the vector database.

---

# 14. Final Data Quality and Approval Checklist

Before enabling production RAG analytics, the following issues must be resolved.

| Area | Required Action |
|---|---|
| Production schema | Reconcile missing production columns. |
| Maintenance schema | Reconcile missing maintenance columns. |
| Work-order schema | Reconcile missing `failure_category` column. |
| Machine schema | Verify threshold-related fields and actual deployed schema. |
| Spare parts | Supply and verify CREATE TABLE definition. |
| Audit logs | Supply and verify CREATE TABLE definition. |
| Attendance | Verify schema and persistence synchronization. |
| Currency | Approve INR or USD standardization. |
| KPI governance | Approve canonical OEE and related KPI formulas. |
| Shift policy | Confirm official A/B/C shift timings. |
| Data relationships | Normalize `Not Linked` values. |
| Numeric anomalies | Convert `-1` sentinels to NULL. |
| Technician IDs | Resolve T01–T08 identity mapping. |
| Supabase security | Align Express authentication and Supabase RLS. |

---

# 15. Final Summary

This document defines the main FactoryOps database tables, operational datasets, KPI calculations, data-cleaning requirements, and recommended structured retrieval functions.

The most important implementation principles are:

1. Use structured database queries for live operational metrics.
2. Use vector retrieval for SOPs, policies, workflows, and reference documentation.
3. Use hybrid retrieval when a question requires both operational data and procedural knowledge.
4. Normalize `Not Linked` placeholders to NULL.
5. Exclude `-1` sentinel values from numerical calculations.
6. Do not assume an unverified currency unit.
7. Do not treat synthetic telemetry as live sensor data.
8. Do not silently reconcile conflicting KPI calculations.
9. Enforce role permissions and factory scope on the backend.
10. Verify the deployed Supabase schema before implementing production analytical tools.

**The FactoryOps RAG assistant must prioritize data accuracy, traceability, and authorization over generating answers from incomplete or inconsistent information.**