# FactoryOps — Maintenance Guidelines

## 1. Purpose

This document describes the maintenance management functionality in the FactoryOps application.

FactoryOps supports maintenance record tracking, maintenance history, downtime and cost monitoring, and work-order coordination.

The RAG assistant should use this document to answer questions about maintenance processes and guidelines. For current maintenance records, it must retrieve information from the operational database rather than relying on static document content.

---

## 2. Maintenance Overview

FactoryOps manages maintenance activities for machines operating at Apex Precision Manufacturing.

| Property | Details |
|---|---|
| Factory | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Total core machines | 24 |
| Machine ID range | M001–M024 |
| Maintenance module | Maintenance Management |
| Database | Supabase PostgreSQL |
| Backend | Node.js + Express + TypeScript |

The maintenance module tracks maintenance activities associated with factory machines.

### Supported maintenance categories

The maintenance dataset contains the following maintenance types:

- Preventive
- Inspection
- Corrective
- Calibration
- Breakdown

The application UI currently exposes these maintenance types:

- Predictive
- Preventive
- Corrective
- Calibration

**Important:** The dataset and UI do not have identical maintenance-type options. The RAG assistant must preserve the distinction instead of assuming that every dataset category is available in the UI.

---

## 3. Maintenance Record Structure

The maintenance dataset contains 210 records and 28 columns.

Maintenance records contain information related to:

- Maintenance record identification
- Associated machine
- Maintenance type
- Maintenance description
- Maintenance status
- Scheduled or recorded maintenance dates
- Technician information
- Downtime
- Maintenance cost
- Related work-order information

The exact available fields should be checked against the live database schema before constructing queries.

### Maintenance dataset status

The supplied cleaned maintenance dataset contains:

| Attribute | Observed value |
|---|---|
| Total records | 210 |
| Maintenance statuses | Completed |
| Date range | 2026-07-02 to 2026-10-02 |
| Maintenance types | Preventive, Inspection, Corrective, Calibration, Breakdown |

These figures describe the supplied dataset, not necessarily the current live database.

---

## 4. Maintenance Priorities

The maintenance dataset contains the following priority levels:

- Low
- Medium
- High
- Critical

However, the current maintenance UI does not expose a priority selector.

The RAG assistant must not assume that users can select or change maintenance priority through the current maintenance interface.

If a user asks about the priority of a specific maintenance record, retrieve the actual record and verify whether a priority value exists.

---

## 5. Maintenance Statuses

The maintenance dataset contains these statuses:

| Status | Meaning |
|---|---|
| Scheduled | Maintenance is planned. |
| In Progress | Maintenance work is underway. |
| Completed | Maintenance activity has been completed. |

These are the statuses identified in the supplied dataset.

The assistant must not claim that a maintenance activity is completed simply because a work order is completed, or vice versa. Maintenance records and work orders are separate operational records.

---

## 6. Maintenance Workflow

The maintenance module supports the tracking of maintenance activities.

A typical maintenance lifecycle can involve:

1. Identifying a machine that requires maintenance.
2. Recording the maintenance activity.
3. Selecting the applicable maintenance type.
4. Recording maintenance information.
5. Tracking the maintenance status.
6. Recording relevant downtime and cost information.
7. Reviewing maintenance history.

The exact steps and available actions depend on the current application implementation and user permissions.

### Important implementation limitation

Creating a maintenance record does not automatically:

- Create a work order.
- Close an existing work order.
- Update the machine's `last_service_date`.

The RAG assistant must not tell users that these actions happen automatically.

---

## 7. Maintenance and Work Order Relationship

Maintenance records and work orders are related operational entities, but they serve different purposes.

| Maintenance Records | Work Orders |
|---|---|
| Record maintenance activities. | Track maintenance or repair tasks. |
| Store maintenance history. | Track task status and lifecycle. |
| Capture maintenance information. | Support assignment and execution. |
| Can contain downtime and cost information. | Can be linked to incidents and maintenance records. |

Some maintenance records reference work orders through text-based identifiers.

The assistant should use actual database relationships and verified identifiers when connecting maintenance records with work orders.

It must not assume that every maintenance record has a linked work order.

---

## 8. Technician Information

Maintenance records contain technician-related information.

The supplied maintenance dataset uses technician IDs:

- T01
- T02
- T03
- T04
- T05
- T06
- T07
- T08

The current application also contains technician profiles using identifiers such as:

- TECH-001
- TECH-002
- TECH-003
- TECH-004
- TECH-005
- TECH-006

These identifier formats do not match directly.

### RAG instruction

Do not assume that `T01` and `TECH-001` represent the same technician.

Before joining technician records, verify the mapping against the actual application data.

If no verified mapping exists, report the original identifier and explain that the identity mapping is unavailable.

---

## 9. Maintenance Cost and Downtime

Maintenance records may contain cost and downtime information.

These metrics can support operational analysis, including:

- Total maintenance cost
- Maintenance cost by machine
- Maintenance cost by maintenance type
- Total maintenance downtime
- Downtime by machine
- Maintenance activity frequency
- Maintenance history over time

### Currency limitation

The currency used in the supplied maintenance and work-order datasets has not been verified.

The assistant must not automatically label maintenance costs as INR, USD, or another currency.

If a user asks for maintenance expenditure, retrieve the actual values and clearly state that the currency is unconfirmed unless the live system provides verified currency information.

### Downtime calculation

When calculating maintenance downtime:

- Use valid downtime values.
- Treat `-1` sentinel values as missing, not actual downtime.
- Do not include missing values as negative downtime.
- Explain the calculation basis when reporting totals or averages.

---

## 10. Maintenance Data Quality

The supplied maintenance dataset has 210 rows and 28 columns.

The following limitations must be considered:

1. Technician identifiers differ from the identifiers used by current technician profiles.
2. Currency information is not verified.
3. Dataset values may not represent current live operational conditions.
4. The database schema and application code have some field differences.
5. The supplied dataset contains completed maintenance records, but live records may have other statuses.

The assistant should validate data before performing joins, calculations, or comparisons.

---

## 11. Maintenance-Related User Roles

FactoryOps uses role-based access control.

Relevant roles include:

| Role | General responsibility |
|---|---|
| SUPER_ADMIN | System-level administration. |
| ADMIN | Factory administration. |
| MANAGER_SUPERVISOR | Operational supervision and maintenance coordination. |
| PRODUCTION_PLANNER | Production planning and operational analysis. |
| TECHNICIAN | Assigned maintenance and repair activities. |

Actual access to maintenance actions must be determined by the backend authorization rules.

The RAG assistant must not grant permissions based only on a user's question or a role supplied by the frontend.

---

## 12. Maintenance Analytics

The assistant may support questions involving:

### Maintenance volume
- How many maintenance records exist?
- How many maintenance activities were completed?
- How many activities are currently in progress?
- How many activities are scheduled?

### Machine maintenance
- Which machines have maintenance records?
- What is the maintenance history of a machine?
- Which machine has the highest recorded maintenance downtime?
- How frequently has a machine undergone maintenance?

### Cost and downtime
- What is the total recorded maintenance cost?
- Which machine has the highest maintenance cost?
- What is the total maintenance downtime?
- How does maintenance downtime vary by month?

### Maintenance types
- How many preventive maintenance activities were recorded?
- How many corrective maintenance activities were recorded?
- What types of maintenance are most frequent?

These questions should be answered using structured database queries against the latest available operational records.

---

## 13. RAG Retrieval Guidelines

The RAG assistant should distinguish between maintenance knowledge questions and live operational questions.

### Knowledge-based questions

Examples:

- What is preventive maintenance?
- What maintenance categories are supported?
- What is the difference between maintenance records and work orders?
- Does creating a maintenance record automatically create a work order?

Use this document and other verified FactoryOps documentation.

### Operational questions

Examples:

- How many maintenance records are completed?
- What is the maintenance history of M005?
- Which machine has the highest maintenance downtime?
- What is the recorded maintenance cost this month?

Use structured database queries.

### Hybrid questions

Examples:

- Explain corrective maintenance and show how many corrective maintenance records exist.
- Explain the maintenance workflow and identify machines with recorded maintenance activities.

Use this document for the explanation and structured database queries for current figures.

---

## 14. Accuracy and Safety Rules

The RAG assistant must follow these rules:

1. Never invent maintenance records.
2. Never assume an unverified technician identity mapping.
3. Never assume the currency of maintenance costs.
4. Treat `-1` downtime or labor values as missing data.
5. Do not assume maintenance completion automatically closes a work order.
6. Do not claim that creating maintenance updates `last_service_date`.
7. Distinguish dataset observations from current live database values.
8. Enforce backend role-based permissions.
9. Do not invent maintenance schedules, intervals, or OEM procedures.
10. If a required field or relationship is unavailable, clearly communicate the limitation.

---

## 15. Important Limitations

The following information is not fully established by the current application analysis:

- Official machine-specific preventive maintenance schedules.
- OEM maintenance manuals.
- Detailed maintenance checklists for every machine.
- Verified technician ID mappings.
- Confirmed maintenance cost currency.
- Automatic maintenance-to-work-order creation.
- Automatic machine last-service-date updates.

The RAG assistant must not generate these details as established FactoryOps functionality.

---

## 16. Summary

FactoryOps provides maintenance record tracking, maintenance history, downtime and cost information, and coordination with work orders and technicians.

The RAG assistant should use documentation for maintenance explanations and verified operational database queries for current maintenance records and analytics.

Accuracy, role-based access control, data validation, and clear communication of missing information are essential.