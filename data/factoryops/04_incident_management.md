# FactoryOps — Incident Management

## 1. Purpose

This document describes the Incident Management module in FactoryOps.

The module allows authorized factory users to report equipment problems, machine stoppages, quality issues, and other operational incidents.

It supports:

- Incident reporting
- Severity classification
- Failure category tracking
- Incident status management
- Work-order escalation
- Technician assignment
- Repair progress tracking
- Manager verification
- Incident resolution and closure

The RAG assistant should use this document to explain incident workflows and retrieve live incident information from the operational database when answering questions about current incidents.

---

## 2. Factory and Incident Overview

| Property | Details |
|---|---|
| Factory | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Factory Code | APX-01 |
| Location | Hyderabad, Telangana |
| Production Lines | L01–L04 |
| Core Machines | M001–M024 |
| Database Table | `incidents` |
| Frontend Page | `IncidentsPage.tsx` |
| Backend | Node.js + Express + TypeScript |

The incident module is part of the FactoryOps operational management system.

Incidents can be associated with machines, production records, maintenance records, and work orders.

---

## 3. Incident Database Structure

The primary database table is:

`incidents`

Important columns include:

| Column | Description |
|---|---|
| id | Internal primary key |
| incident_id | Unique incident identifier, such as INC-0001 |
| production_id | Associated production record identifier |
| maintenance_id | Associated maintenance record identifier |
| factory_id | Associated factory |
| machine_id | Machine identifier |
| machine_name | Machine name |
| line_id | Production line identifier |
| line_name | Production line name |
| station_number | Station number |
| product_id | Associated product identifier |
| product_name | Product name |
| incident_type | Type of incident |
| severity | Incident severity |
| failure_category | Failure classification |
| title | Incident title |
| problem_description | Description of the problem |
| description | Additional incident description |
| root_cause | Identified root cause |
| action_taken | Corrective action taken |
| downtime_minutes | Downtime caused by the incident |
| defect_units | Defective units associated with the incident |
| status | Current incident status |
| reported_by | User who reported the incident |
| technician_id | Associated technician identifier |
| technician_name | Technician name |
| reported_at | Incident reporting timestamp |
| resolved_at | Incident resolution timestamp |
| resolution_notes | Resolution details |
| remarks | Additional remarks |

### Relationship limitation

The `machine_id`, `production_id`, and `maintenance_id` columns are plain text fields in the inspected SQL schema. They do not have formal foreign-key constraints.

The RAG assistant must validate identifiers before joining incident records with other operational tables.

---

## 4. Incident Identifiers

Incidents use identifiers in the following format:

`INC-0001`

Examples:

- INC-0001
- INC-0002
- INC-0003

The identifier uniquely identifies an incident record.

The assistant should use `incident_id` when users ask about a specific incident.

---

## 5. Failure Categories

FactoryOps uses eight failure categories in the supplied incident dataset.

| Failure Category | Description |
|---|---|
| Sensor/Optical | Sensor or optical-system-related failures |
| Mechanical | Mechanical equipment problems |
| Tooling | Tooling-related failures |
| Hydraulic | Hydraulic-system problems |
| Electrical | Electrical-system failures |
| Chemical | Chemical-related incidents |
| Thermal/Cooling | Temperature or cooling-related failures |
| Pneumatic | Pneumatic-system problems |

These categories classify the failure associated with an incident.

The assistant must not invent additional official failure categories.

---

## 6. Incident Types

The `incident_type` field records the type of incident.

The supplied dataset includes machine stoppage, quality-related issues, and equipment failure types.

The assistant should retrieve the actual `incident_type` value when answering questions about a specific incident.

It must not assume that `incident_type` and `failure_category` represent the same field.

- `incident_type` describes the recorded incident type.
- `failure_category` classifies the failure.

---

## 7. Incident Severity Levels

FactoryOps supports four severity levels.

| Severity | General meaning |
|---|---|
| Low | Lower-severity incident |
| Medium | Moderate-severity incident |
| High | High-severity incident |
| Critical | Critical incident requiring urgent attention |

The `severity` field has a default value of `Medium` in the inspected database schema.

### Severity and work-order priority mapping

When an incident is escalated through the work-order creation interface, its severity is mapped to work-order priority as follows:

| Incident Severity | Work Order Priority |
|---|---|
| Critical | Critical |
| High | High |
| Medium | Medium |
| Low | Medium |

There is no separate priority column in the incident table.

The assistant must distinguish between incident severity and work-order priority.

### Important limitation

Official incident response-time targets and resolution SLAs have not been established in the inspected application documentation.

Do not invent response deadlines or escalation timelines.

---

## 8. Incident Status Lifecycle

The application supports the following incident statuses:

| Status | Meaning |
|---|---|
| Open | Incident has been reported. |
| Assigned | Incident has been assigned for handling. |
| Investigating | Incident is under investigation. |
| In Progress | Work is actively being performed. |
| Resolved | A resolution has been submitted or recorded. |
| Closed | Incident has completed the required closure process. |

### Dataset versus application statuses

The supplied cleaned incident dataset contains 109 records with these observed statuses:

- Closed
- Investigating

The application supports a broader lifecycle.

The assistant must not assume that the dataset contains every status supported by the application.

---

## 9. Incident Reporting Workflow

The following roles can report incidents:

- ADMIN
- SUPER_ADMIN
- MANAGER_SUPERVISOR
- TECHNICIAN

### Reporting process

1. The authorized user opens the Incidents page.
2. The user opens the incident creation form.
3. The user provides the machine identifier.
4. The user enters an incident title.
5. The user selects a severity.
6. The user provides a problem description.
7. The frontend submits the incident to the backend.
8. The backend creates an incident with a generated `INC-*` identifier and status `Open`.

### API

`POST /api/incidents`

The backend handles incident creation and persistence.

---

## 10. Incident Escalation

FactoryOps supports two main incident escalation paths.

### Path A: Work Order Escalation

Managers and administrators can escalate an incident by creating a work order.

The application opens the work-order creation form with relevant information prefilled, including:

- Incident ID
- Machine ID
- Incident title
- Mapped work-order priority

The work order provides a structured way to track the maintenance or repair task.

### Path B: Technician Assignment

Managers can use the Technician Assignment workflow to assign an incident-related repair task to a suitable technician.

The workflow includes:

1. Technician recommendation.
2. Manager review.
3. Technician dispatch.
4. Technician acceptance or rejection.
5. Repair execution.
6. Progress updates.
7. Resolution submission.
8. Manager verification.

This workflow supports controlled repair execution and segregation of duties.

---

## 11. Technician Recommendation System

FactoryOps includes a technician recommendation mechanism.

The recommendation logic is implemented in `server/db.ts`.

It uses deterministic, rule-based scoring rather than an LLM.

### Factors considered

- Primary specialization match
- Secondary specialization match
- Other specialization match
- Technician skill matches
- Technician availability
- Active assignment workload
- Technician rating
- Technician experience

### Scoring rules

| Factor | Score |
|---|---:|
| Primary specialization match | +50 |
| Secondary specialization match | +28 |
| Other specialization match | +10 |
| Each matched skill | +8 |
| Available technician | +20 |
| Busy technician | +5 |
| Other availability states | -40 |
| Each active assignment | -6 |

Additional rating and experience bonuses are also considered.

The final score is normalized using:

`(score / 115) * 100`

The resulting recommendation percentage is clamped between 35% and 99%.

### Important distinction

This is a rule-based technician matching mechanism.

The RAG assistant must not describe it as an autonomous LLM-based technician selection system.

Managers remain responsible for reviewing and dispatching assignments.

---

## 12. Technician Assignment State Machine

The technician assignment workflow follows this state sequence:

`PENDING ACCEPTANCE → ACCEPTED → IN PROGRESS → RESOLVED_PENDING_VERIFICATION → VERIFIED`

### Detailed workflow

**1. PENDING ACCEPTANCE**

The manager dispatches an assignment to a technician.

**2. ACCEPTED**

The technician accepts the assigned task.

The technician may instead reject the assignment or request reassignment.

**3. REJECTED**

The technician rejects the assignment and must provide a reason.

**4. REASSIGNMENT_REQUESTED**

The technician requests reassignment and must provide a reason.

The manager reviews the request.

**5. IN PROGRESS**

The technician starts the repair and can submit progress updates.

**6. RESOLVED_PENDING_VERIFICATION**

The technician submits the repair resolution for manager verification.

**7. VERIFIED**

The manager verifies and signs off the completed repair.

### Verification rejection

If the manager rejects the submitted resolution:

- The assignment returns to `IN PROGRESS`.
- Progress is reset to 75%.
- The technician is notified.

The technician can continue the repair and submit the resolution again.

---

## 13. Repair Verification and Segregation of Duties

FactoryOps enforces separation between repair execution and repair verification.

### Important rule

A technician cannot verify or sign off their own repair.

The backend checks whether the assignment is a self-repair before allowing verification.

The exception is `SUPER_ADMIN`.

### Verification API

`POST /api/technician-assignments/:id/verify`

The manager performs verification through this endpoint.

### Verified closure behavior

When an assignment is successfully verified:

- The linked incident is updated to `Closed`.
- The incident's `resolved_at` field is updated.
- Resolution information is synchronized, including:
  - `root_cause`
  - `action_taken`
  - `resolution_notes`
- The linked work order is also updated.
- Relevant real-time notifications are generated.

This automatic synchronization occurs through the verified technician assignment closure workflow.

It should not be confused with simply creating a maintenance record.

---

## 14. Incident Metrics and Analytics

FactoryOps supports several incident-related operational metrics.

### Total Incident Count

The total number of incident records.

### Open or Active Incident Count

The number of incidents that are currently active.

The assistant should use the application's verified status definitions when determining which statuses count as active.

### Incident Severity Distribution

The number of incidents grouped by:

- Low
- Medium
- High
- Critical

### Failure Category Distribution

The number of incidents grouped by failure category.

### Downtime by Machine

The total recorded incident downtime for each machine.

Formula:

`Total Incident Downtime = SUM(downtime_minutes)`

### Defect Units Impact

The total number of defective units associated with incidents.

Formula:

`Total Defect Units Impact = SUM(defect_units)`

All current counts and aggregations should come from structured database queries.

### Dashboard calculation limitation

The Manager and Technician dashboard incident-severity charts contain hardcoded percentage labels.

The Admin dashboard calculates the percentages dynamically.

Therefore, the RAG assistant should calculate severity percentages from actual incident records rather than copying static chart labels.

---

## 15. Incident Dataset Information

The supplied cleaned incident dataset contains:

| Attribute | Observed Value |
|---|---|
| Total records | 109 |
| Date range | 2026-07-01 to 2026-09-08 |
| Observed statuses | Closed, Investigating |
| Failure categories | 8 |

These figures describe the supplied dataset, not necessarily the current live database.

### Data quality considerations

The dataset contains some incomplete relationship references:

- One `production_id` contains `Not Linked`.
- 41 `maintenance_id` values contain `Not Linked`.

Treat these placeholders as missing values.

Do not use `Not Linked` as an actual database identifier or join key.

---

## 16. Role-Based Incident Responsibilities

| Role | Incident Responsibility |
|---|---|
| SUPER_ADMIN | System-level oversight and authorized administration. |
| ADMIN | Incident reporting, administration, and escalation. |
| MANAGER_SUPERVISOR | Incident reporting, escalation, technician assignment, and repair verification. |
| PRODUCTION_PLANNER | Operational planning and authorized incident visibility. |
| TECHNICIAN | Incident reporting, assigned repair execution, and resolution submission. |

Actual access must be determined by backend authorization rules.

The assistant must not assume that every role can perform every incident action.

Production Planner access to assignment information also has restrictions: rejection and reassignment reasons are redacted.

---

## 17. RAG Retrieval Guidelines

The assistant should identify whether a question requires incident documentation, live operational data, or both.

### Knowledge-based questions

Examples:

- What are the incident severity levels?
- What are the failure categories?
- How does incident escalation work?
- Can a technician verify their own repair?
- How does technician recommendation work?

Use this document and other verified FactoryOps documentation.

### Operational questions

Examples:

- How many incidents are currently open?
- Show all critical incidents.
- Which machine has the highest incident downtime?
- How many incidents belong to the Mechanical category?
- What is the status of INC-0001?

Use structured database queries against the `incidents` table.

### Hybrid questions

Examples:

- Explain the incident escalation process and show how many incidents are currently open.
- Explain technician verification and identify incidents awaiting verification.
- Explain severity levels and show the current severity distribution.

Use documentation for explanations and structured queries for current operational information.

---

## 18. Accuracy and Safety Rules

The RAG assistant must follow these rules:

1. Never invent incident records or identifiers.
2. Never invent incident response or resolution SLAs.
3. Distinguish incident severity from work-order priority.
4. Do not confuse `incident_type` with `failure_category`.
5. Validate text-based identifiers before joining database records.
6. Treat `Not Linked` values as missing references.
7. Do not claim that technician recommendation is performed by an LLM.
8. Never allow a technician to verify their own repair.
9. Do not claim that an incident is closed before the required verification process.
10. Use live database queries for current incident counts and status information.
11. Enforce backend role-based permissions.
12. Do not expose restricted rejection or reassignment reasons to unauthorized roles.
13. Clearly distinguish supplied dataset statistics from live operational statistics.

---

## 19. Important Limitations

The following information is not established by the inspected application:

- Official incident response-time SLAs.
- Official incident resolution-time SLAs.
- Severity-based mandatory response deadlines.
- A formal escalation timeline involving additional management levels.
- A complete safety incident investigation policy.

These details require approval from the appropriate factory stakeholders.

The RAG assistant must not generate them as official FactoryOps policies.

---

## 20. Summary

FactoryOps provides an incident management workflow covering incident reporting, severity classification, escalation, technician assignment, repair progress, manager verification, and incident closure.

The technician recommendation mechanism uses deterministic rule-based scoring.

Repair verification enforces segregation of duties, preventing technicians from verifying their own repairs.

The RAG assistant should use documentation for incident-process explanations and structured operational queries for current incident records, metrics, and status information.