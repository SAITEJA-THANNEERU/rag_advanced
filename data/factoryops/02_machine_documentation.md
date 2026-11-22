# FactoryOps – Machine Documentation

## 1. Introduction

FactoryOps maintains a centralized machine registry for Apex Precision Manufacturing (FAC-001).

The machine management module provides information about factory equipment, production-line assignments, machine specifications, operational status and available machine health indicators.

Machines are important operational assets because they are connected to production records, maintenance activities, incidents and work orders.

This document describes the machine information and monitoring functionality available in FactoryOps.

## 2. Factory Machine Overview

| Attribute | Details |
|---|---|
| Factory Name | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Factory Code | APX-01 |
| Location | Hyderabad, Telangana, India |
| Production Lines | 4 |
| Core Machines | 24 |
| Machine ID Range | M001–M024 |
| Station Range | ST-01–ST-06 |

The current application operates in single-factory mode.

The factory contains four production lines, with six core machine stations per line.

## 3. Production Line Structure

FactoryOps organizes machines into four production lines.

| Line ID | Production Line | Core Stations |
|---|---|---|
| L01 | Machining Line 1 | ST-01 to ST-06 |
| L02 | Stamping Line 2 | ST-01 to ST-06 |
| L03 | Welding Line 3 | ST-01 to ST-06 |
| L04 | Coating & Packaging Line 4 | ST-01 to ST-06 |

Each production line contains six core machine stations.

**Important:** The available analysis confirms the overall machine count and line structure but does not provide a verified individual M001–M024 machine-to-line mapping. Do not invent individual assignments.

## 4. Machine Identification

FactoryOps uses machine identifiers to associate equipment with operational records.

| Identifier | Description |
|---|---|
| M001–M024 | Core machine identifiers |
| L01–L04 | Production line identifiers |
| ST-01–ST-06 | Station identifiers |

Machine records may contain the following identification information:

- Machine ID.
- Machine name.
- Machine type.
- Production line.
- Station number.
- Manufacturer.
- Model.
- Serial number.

These identifiers are important when retrieving machine-specific production, maintenance, incident and work order information.

## 5. Machine Database Structure

The primary Supabase database table is:

`machines`

The verified SQL schema includes the following fields.

| Column | Data Type | Description |
|---|---|---|
| id | TEXT | Primary machine record identifier |
| factory_id | TEXT | Associated factory identifier |
| machine_id | TEXT | Unique machine identifier |
| name | TEXT | Machine name |
| type | TEXT | Machine category |
| line | TEXT | Production line |
| station_number | TEXT | Station identifier |
| manufacturer | TEXT | Equipment manufacturer |
| model | TEXT | Machine model |
| serial_number | TEXT | Machine serial number |
| target_cycle_time_seconds | NUMERIC | Target cycle time |
| rated_capacity_uph | NUMERIC | Rated units per hour |
| power_rating_kw | NUMERIC | Power rating in kilowatts |
| maintenance_interval_days | NUMERIC | Maintenance interval |
| status | TEXT | Machine operational status |
| health_score | NUMERIC | Machine health indicator |
| temperature_c | NUMERIC | Temperature reading |
| vibration_mms | NUMERIC | Vibration reading |
| pressure_bar | NUMERIC | Pressure reading |
| speed_rpm | NUMERIC | Rotational speed |
| oee | NUMERIC | Machine OEE indicator |
| operator | TEXT | Assigned operator |
| install_date | DATE | Installation date |
| last_service_date | DATE | Last service date |

The application and data mappings also use alternative naming conventions such as `machine_name`, `machine_type`, `line_id` and `line_name`.

The actual deployed Supabase schema must be verified before production queries are implemented.

## 6. Machine Technical Specifications

The machine dataset contains technical specifications for the 24 core machines.

| Specification | Verified Dataset Range |
|---|---|
| Target Cycle Time | 44–96 seconds |
| Rated Capacity | 38–82 units/hour |
| Power Rating | 6–55 kW |
| Maintenance Interval | 30, 45 or 60 days |

These are ranges across the dataset, not specifications applicable to every machine.

Individual machine specifications must be retrieved from the corresponding machine record.

### 6.1 Maintenance Intervals

The machine dataset contains maintenance intervals of:

- 30 days.
- 45 days.
- 60 days.

These values represent recorded maintenance interval settings.

Detailed preventive maintenance checklists for each interval are not currently verified.

## 7. Machine Operational Status

FactoryOps uses machine status information to represent equipment availability and operational conditions.

The application recognizes these primary status values:

| Status | Description |
|---|---|
| running | Machine is operating |
| warning | Machine has a warning condition |
| maintenance | Machine is undergoing maintenance |
| offline | Machine is unavailable |

The application also contains status normalization for values such as:

- Active.
- Operational.
- Faulted.
- Inactive.

Historical CSV records use `Active` for all 24 original machine records.

The application normalizes certain status values when displaying machine information.

**Important:** Historical dataset status values and current application status values are not necessarily identical.

The RAG assistant should retrieve the current status from the operational database rather than assuming the historical CSV status is still valid.

## 8. Machine Health and Telemetry

FactoryOps displays machine health indicators and operational measurements.

The available fields include:

| Metric | Unit | Description |
|---|---|---|
| Health Score | % | Machine health indicator |
| Temperature | °C | Machine temperature |
| Vibration | mm/s | Machine vibration |
| Pressure | bar | Operating pressure |
| Speed | RPM | Machine rotational speed |
| OEE | % | Overall Equipment Effectiveness |

### 8.1 Important Telemetry Limitation

The current machine dataset does not contain original temperature, vibration, pressure, speed, health score or OEE sensor readings.

These values are synthetically generated during the application's initial data seeding process.

There is currently no verified live PLC or IoT sensor ingestion pipeline.

Therefore:

1. Do not describe the displayed values as verified real-time physical sensor measurements.
2. Do not claim that a machine has experienced a physical failure based only on synthetic telemetry.
3. Retrieve available values from the current application database when requested.
4. Clearly communicate that telemetry is synthetic where relevant.
5. Do not invent missing sensor measurements.

## 9. Machine Threshold Configuration

FactoryOps includes a machine threshold configuration interface.

The application currently contains the following threshold values in its UI configuration:

| Parameter | UI Default |
|---|---|
| Maximum Temperature | 75°C |
| Maximum Vibration | 3.5 mm/s |

There is also a different threshold display in the machine detail interface showing a temperature threshold of 85°C.

This is a verified configuration inconsistency.

Additionally, the fields `max_temperature_c` and `max_vibration_mms` are absent from the supplied `machines` table SQL definition.

Their persistence in the live Supabase database has not been verified.

**RAG instruction:** Never treat these displayed values as approved universal machine safety limits. Do not recommend operating or maintenance decisions based solely on them.

## 10. Machine Management Workflows

FactoryOps provides the following machine management operations.

### 10.1 Machine Registration

Authorized users can add machine records through the machine management interface.

### 10.2 Machine Updates

Machine information can be edited by authorized administrative and management users.

### 10.3 Machine Status Updates

The application supports machine status changes through:

`PATCH /api/machines/:id/status`

### 10.4 Machine Threshold Configuration

Threshold settings can be configured through:

`POST /api/machines/thresholds`

### 10.5 Machine Deletion

Machine deletion is restricted to ADMIN and SUPER_ADMIN roles.

Exact permission enforcement must follow the backend authorization implementation.

## 11. Machine Relationships with Other Modules

Machine records are associated with several FactoryOps operational modules.

| Related Module | Database Table | Relationship |
|---|---|---|
| Production | production_records | machine_id |
| Maintenance | maintenance_records | machine_id |
| Incidents | incidents | machine_id |
| Work Orders | work_orders | machine_id |
| Data Quality | data_quality_metrics | machine_id |
| Technician Assignments | technician_incident_assignments | machine_id |

These operational relationships primarily use machine identifiers as text-based references.

Not all relationships are enforced through SQL foreign keys.

### 11.1 Machine and Production

Production records identify the machine responsible for a production run.

Machine-related production analysis can include:

- Total production.
- Defective units.
- Production downtime.
- Production by shift.
- Machine-wise defect rate.

### 11.2 Machine and Maintenance

Maintenance records contain information about servicing activities performed on machines.

This includes:

- Maintenance type.
- Maintenance status.
- Technician.
- Scheduled date.
- Completed date.
- Downtime.
- Maintenance cost.
- Action taken.

### 11.3 Machine and Incidents

Incidents can be associated with machines to record operational problems.

Information can include:

- Incident severity.
- Failure category.
- Problem description.
- Root cause.
- Downtime.
- Defect impact.
- Resolution information.

### 11.4 Machine and Work Orders

Work orders can be associated with machines to coordinate repair and maintenance activities.

Information can include:

- Work order type.
- Priority.
- Status.
- Assigned technician.
- Due date.
- Parts requirements.
- Completion information.

## 12. Machine Performance Metrics

FactoryOps provides several machine-related operational metrics.

| Metric | Description |
|---|---|
| Machine Health Score | Health indicator associated with a machine |
| Machine OEE | Overall Equipment Effectiveness |
| Total Production | Units produced by a machine |
| Defect Rate | Percentage of defective units |
| Cumulative Downtime | Total recorded downtime |
| Temperature | Recorded temperature value |
| Vibration | Recorded vibration value |

### 12.1 Machine-Wise Defect Rate

The application uses the following calculation:

`Defect Rate (%) = (Total Defect Units / Total Actual Units) × 100`

### 12.2 Machine-Wise Cumulative Downtime

`Cumulative Downtime = Sum of Recorded Downtime Minutes`

These calculations should use actual operational records rather than values generated by the language model.

## 13. Data Quality and Known Limitations

The following limitations must be considered when processing machine information.

1. The original machine CSV contains 24 records.
2. All 24 original machine records have the status `Active`.
3. The persistent store contains 28 machine records because four additional runtime/test records were added.
4. Historical machine specifications must not automatically be treated as current operating conditions.
5. Machine telemetry is synthetically generated.
6. The supplied SQL schema does not contain the configured maximum temperature and vibration threshold columns.
7. The live Supabase database schema has not yet been independently verified.
8. Detailed OEM manuals and alarm/fault-code documentation are not available in the current analysis.

## 14. Missing Machine Documentation

The following information is required to build a more complete machine knowledge base.

| Missing Information | Purpose |
|---|---|
| OEM Machine Manuals | Manufacturer-specific operating instructions |
| Machine Alarm Codes | Identify equipment faults |
| Troubleshooting Procedures | Guide maintenance investigations |
| Lubrication Charts | Support preventive maintenance |
| Torque Specifications | Support equipment servicing |
| Approved Operating Limits | Define safe operating conditions |
| Machine-Specific Maintenance Checklists | Support 30/45/60-day servicing |
| Approved Sensor Thresholds | Support reliable monitoring |

These details must be obtained from manufacturer documentation or approved plant engineering records.

Do not generate fictional machine specifications or safety limits.

## 15. Advanced RAG Retrieval Requirements

The FactoryOps RAG Assistant should use this document for machine-related knowledge questions.

### 15.1 Knowledge-Based Questions

Examples:

- How are machines organized in FactoryOps?
- How many production lines are available?
- What does machine health score represent?
- What machine information is maintained by the application?
- What does the maintenance interval field represent?

These questions can be answered using this document.

### 15.2 Live Database Questions

Examples:

- What is the current status of machine M007?
- Which production line contains machine M012?
- What is the recorded temperature of machine M005?
- Show the maintenance history of M009.
- Which incidents are associated with M003?
- What is the total downtime of machine M015?

These questions require structured retrieval from the original FactoryOps Supabase database.

### 15.3 Hybrid Questions

Examples:

- Machine M007 has recorded high downtime. What maintenance information is available?
- What does the machine maintenance interval mean, and when was M003 last serviced?
- Which incidents are associated with a machine, and what troubleshooting documentation is available?

These questions require both documentation retrieval and operational database queries.

## 16. RAG Accuracy and Safety Rules

The RAG assistant must follow these rules:

1. Use verified machine documentation.
2. Retrieve current machine information from the operational database.
3. Never assume historical records represent current machine status.
4. Clearly distinguish synthetic telemetry from actual sensor measurements.
5. Do not invent machine specifications.
6. Do not invent OEM alarm codes or troubleshooting instructions.
7. Do not treat unapproved UI thresholds as official safety limits.
8. Respect the authenticated user's machine and operational data permissions.
9. Use machine IDs to retrieve related operational records.
10. State clearly when requested machine information is unavailable.

---

**Document:** 02_machine_documentation.md  
**Project:** FactoryOps – AI Smart Factory Operations & Maintenance Platform  
**Knowledge Base:** FactoryOps Advanced RAG  
**Status:** Initial knowledge document – pending project-owner review