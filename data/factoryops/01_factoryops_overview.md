# FactoryOps – Application Overview

## 1. Introduction

FactoryOps, officially known as the **AI Smart Factory Operations & Maintenance Platform**, is a full-stack web application designed to centralize and manage manufacturing plant operations.

The platform provides a unified environment for monitoring machines, tracking production, managing maintenance activities, handling operational incidents, coordinating work orders, managing spare parts, monitoring workforce attendance and accessing Standard Operating Procedures (SOPs).

FactoryOps aims to improve operational visibility, maintenance coordination, production monitoring and decision-making through centralized data management and role-based access control.

## 2. Project Information

| Attribute | Details |
|---|---|
| Application Name | FactoryOps |
| Full Name | AI Smart Factory Operations & Maintenance Platform |
| Manufacturing Facility | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Factory Code | APX-01 |
| Location | Hyderabad, Telangana, India |
| Operating Mode | Single-Factory Mode |
| Production Lines | 4 |
| Core Machines | 24 |
| Primary Database | Supabase PostgreSQL |
| Frontend | React, TypeScript and Vite |
| Backend | Node.js and Express |
| AI Integration | Google Gemini (existing basic chatbot) |

The application currently operates in single-factory mode for FAC-001. Multi-factory capabilities are present in some legacy and platform-level code but are not currently enabled for active operations.

## 3. Problem Statement

Manufacturing operations involve several interconnected activities, including machine monitoring, production tracking, quality management, maintenance scheduling, incident resolution and workforce coordination.

When these activities are managed independently, plant teams can experience difficulties accessing operational information, identifying recurring equipment problems, coordinating maintenance and understanding production performance.

FactoryOps addresses these challenges by providing a centralized operational platform with role-specific dashboards, structured workflows and shared operational information.

## 4. Project Objectives

The primary objectives are:

1. Centralize manufacturing operations and operational records.
2. Monitor machine health and equipment status.
3. Track production performance across machines and shifts.
4. Record and manage maintenance activities.
5. Report, investigate and resolve operational incidents.
6. Coordinate work orders and technician assignments.
7. Manage spare parts inventory.
8. Monitor workforce attendance through GPS-based geofencing.
9. Provide access to operational SOPs and safety procedures.
10. Enforce role-based access control and segregation of duties.
11. Provide operational dashboards and analytical insights.
12. Introduce an advanced AI-powered assistant for contextual factory information retrieval.

## 5. Application Architecture

FactoryOps uses a full-stack web architecture.

### 5.1 Frontend

Technologies:
- React 19
- TypeScript
- Vite
- Tailwind CSS
- Recharts
- Lucide React
- Motion

Responsibilities:

- Render application pages and dashboards.
- Provide role-specific navigation.
- Display operational records and analytics.
- Handle user interactions and forms.
- Communicate with backend APIs.
- Display notifications and chatbot conversations.

The application uses custom contexts for routing, authentication, application data and filtering.

### 5.2 Backend

Technologies:
- Node.js
- Express
- TypeScript

The backend handles:

- REST API endpoints.
- Authentication and session management.
- Role-based authorization.
- Operational data processing.
- Database communication.
- Business-rule validation.
- Audit logging.
- Real-time notification delivery using Server-Sent Events (SSE).

### 5.3 Database

FactoryOps uses Supabase PostgreSQL for cloud data persistence.

The application also has a local persistent JSON storage fallback.

The persistence adapter attempts to communicate with Supabase and can fall back to local persistent storage when cloud operations are unavailable or blocked.

The local persistent store is located at:

`server/data/persistent-store.json`

**Important:** The actual live Supabase schema must be verified independently before implementing production RAG database queries.

## 6. Main Application Modules

### 6.1 Dashboard

Provides role-specific operational dashboards.

Dashboard information includes:

- Machine status.
- Production performance.
- Maintenance information.
- Incident statistics.
- Work order status.
- Operational KPIs.
- Charts and analytical visualizations.

### 6.2 Machine Management

Maintains the factory machine registry.

Features include:

- Machine registration.
- Machine information management.
- Machine status updates.
- Machine specifications.
- Machine health information.
- Temperature and vibration display.
- Machine threshold configuration.
- Machine-related production and maintenance history.

The current application contains 24 core machines, identified from M001 to M024.

### 6.3 Production Management

Manages production records across machines and shifts.

Features include:

- Production logging.
- Planned versus actual production.
- Production targets.
- Defect tracking.
- Scrap monitoring.
- Downtime tracking.
- Cycle-time information.
- OEE-related analytics.

Production records are associated with machines, production lines, products and shifts.

### 6.4 Maintenance Management

Maintains machine maintenance records and servicing information.

Features include:

- Maintenance logging.
- Maintenance history.
- Maintenance type classification.
- Technician information.
- Downtime tracking.
- Maintenance duration.
- Maintenance costs.
- Parts replacement information.

### 6.5 Incident Management

Provides functionality for reporting and managing operational incidents.

Features include:

- Incident reporting.
- Incident severity classification.
- Failure category tracking.
- Incident status updates.
- Root-cause information.
- Resolution notes.
- Downtime and defect impact tracking.
- Escalation to work orders.
- Technician assignment workflows.

### 6.6 Work Order Management

Coordinates maintenance and operational work.

Features include:

- Work order creation.
- Work order assignment.
- Priority management.
- Status tracking.
- Technician coordination.
- Parts requirement tracking.
- Work completion.
- Manager verification.

Work orders can be created independently or associated with incidents.

### 6.7 Technician Assignment Management

Supports manager-controlled technician assignment and repair verification.

The workflow includes:

1. Manager requests technician recommendations.
2. The system evaluates technician specialization, skills and workload.
3. Manager assigns the incident to a technician.
4. Technician accepts or rejects the assignment.
5. Technician starts the repair.
6. Technician updates repair progress.
7. Technician submits the resolution.
8. Manager verifies the repair.
9. Verified resolution updates the associated incident and work order.

The technician recommendation mechanism is currently rule-based rather than an LLM-powered recommendation system.

### 6.8 Spare Parts Inventory

Manages spare parts and inventory information.

Features include:

- Spare parts registration.
- Stock quantity tracking.
- Category management.
- Supplier information.
- Restocking.
- Minimum reorder level configuration.
- Low-stock alerts.
- Spare parts association with work orders.

### 6.9 Attendance and Geofencing

Manages workforce attendance using GPS-based location validation.

Features include:

- GPS-based check-in.
- Factory geofence validation.
- Attendance records.
- Absence reporting.
- Manager attendance monitoring.
- Administrative attendance oversight.
- Attendance audit logging.

The implemented geofence radius is 1,000 metres from the configured factory location.

### 6.10 SOP Management

Provides access to Standard Operating Procedures.

Features include:

- SOP listing.
- SOP details.
- Step-by-step instructions.
- Safety precautions.
- Interactive checklist execution.

The current SOP checklist sign-off is maintained in frontend React state and is not persisted to the backend.

### 6.11 Analytics and Quality Management

Provides operational performance analysis.

Includes:

- Overall Equipment Effectiveness (OEE).
- Availability.
- Performance.
- Quality.
- First-Pass Yield.
- Defective units.
- Scrap.
- Machine performance comparisons.
- Production analytics.

Some displayed metrics are calculated from application data, while certain labels are currently hardcoded.

### 6.12 Data Quality Management

Provides a view of seeded IoT sensor data-quality metrics.

Features include:

- Sensor data-quality indicators.
- Sensor health cards.
- CSV export.

This module currently uses seeded metrics rather than a live IoT ingestion pipeline.

### 6.13 Notifications and Audit Logs

FactoryOps supports:

- Real-time notification delivery through SSE.
- Assignment notifications.
- Incident resolution notifications.
- Repair verification notifications.
- System audit logs.
- User notification management.

## 7. Factory Structure

The active factory contains four production lines.

| Line ID | Production Line |
|---|---|
| L01 | Machining Line 1 |
| L02 | Stamping Line 2 |
| L03 | Welding Line 3 |
| L04 | Coating & Packaging Line 4 |

Each production line contains six core machine stations, giving a total of 24 core machines.

Machine identifiers follow the convention M001–M024.

Station identifiers follow the convention ST-01–ST-06 within each production line.

## 8. Operational Data Categories

FactoryOps maintains several important categories of operational information.

| Data Category | Database Table | Description |
|---|---|---|
| Factory | factories | Factory information |
| Machines | machines | Machine registry and machine information |
| Production | production_records | Production shift records |
| Maintenance | maintenance_records | Machine maintenance history |
| Incidents | incidents | Operational incident records |
| Work Orders | work_orders | Maintenance and operational work |
| SOPs | sops | Standard Operating Procedures |
| Inventory | spare_parts | Spare parts information |
| Users | users | Application user information |
| Technician Profiles | technician_profiles | Technician skills and profiles |
| Technician Assignments | technician_incident_assignments | Technician assignment workflow |
| Notifications | notifications | User notifications |
| Audit Logs | system_audit_logs | System activity records |

Additional workflow and attendance tables are defined or referenced in the project's SQL and backend implementation. Their live availability must be verified before querying them.

## 9. FactoryOps Operational Workflow

The main operational workflow connects machine monitoring, production, incidents, maintenance and work orders.

### Step 1: Machine Operations

Machines operate across the four production lines.

The system maintains machine information, status and available operational metrics.

### Step 2: Production Monitoring

Production activities are recorded against machines and shifts.

The application tracks planned production, actual production, defects, downtime and related performance metrics.

### Step 3: Incident Reporting

When operational issues occur, authorized users can report incidents.

Incidents contain information such as:

- Machine identification.
- Incident title.
- Severity.
- Failure category.
- Problem description.
- Downtime.
- Defect impact.
- Resolution information.

### Step 4: Work Order or Technician Assignment

Managers can escalate incidents into work orders or use the technician assignment workflow.

Technicians perform assigned repairs and provide progress updates.

### Step 5: Repair Verification

Managers verify submitted repair resolutions.

Successful verification updates linked incident and work order records.

### Step 6: Maintenance Recording

Maintenance activities are recorded to maintain servicing history, downtime and cost information.

### Step 7: Operational Monitoring

Dashboards and analytics provide visibility into machine performance, production, maintenance, incidents and work orders.

## 10. User Roles

FactoryOps defines five primary roles.

| Role | Main Responsibility |
|---|---|
| SUPER_ADMIN | Platform-level administration and factory oversight |
| ADMIN | Factory administration and operational management |
| MANAGER_SUPERVISOR | Production supervision, incident coordination and technician management |
| PRODUCTION_PLANNER | Production planning and work order visibility |
| TECHNICIAN | Assigned repair activities, maintenance and incident updates |

Access is controlled through frontend route permissions and backend authorization.

The actual permissions and restrictions for each role are documented separately in:

`07_user_roles_permissions.md`

## 11. Existing AI Assistant

FactoryOps currently includes a basic Gemini-powered AI chatbot.

Frontend components:

- `src/components/AIChatLauncher.tsx`
- `src/components/AIChatModal.tsx`

Backend endpoints:

- `GET /api/ai/status`
- `POST /api/ai/chat`

The existing chatbot uses prompt-based context injection rather than a full retrieval-augmented generation architecture.

Its current context includes a limited selection of factory KPIs, machines, incidents, work orders and SOP titles.

It does not currently implement:

- Semantic vector retrieval.
- Full operational database querying.
- Hybrid retrieval.
- Document citations.
- Comprehensive role-scoped retrieval.
- Advanced RAG conversational memory.

Upgrading this existing chatbot with an Advanced RAG backend is a planned enhancement.

## 12. Planned AI Enhancements

The broader FactoryOps project identifies the following AI capabilities as future enhancements:

1. Advanced RAG-based SOP and maintenance assistant.
2. Visual defect detection using computer vision.
3. Predictive maintenance.
4. AI-assisted incident triage and root-cause recommendations.
5. Production anomaly detection.

These capabilities must be distinguished from currently implemented functionality.

## 13. Important Data and System Limitations

The following limitations must be considered when answering FactoryOps questions.

### 13.1 Synthetic Machine Telemetry

Temperature, vibration, pressure, speed, health score and OEE values are synthetically generated in the current application seed process.

There is no verified live PLC or IoT sensor ingestion pipeline.

Therefore, the AI assistant must not describe these values as real-time physical sensor measurements.

### 13.2 Production and Maintenance Data

The application contains historical production and maintenance records.

Live database queries must be used when answering questions about current operational status and numerical aggregations.

### 13.3 Multi-Factory Support

The active application currently enforces FAC-001.

Multi-factory operations are not currently enabled.

### 13.4 SOP Sign-Off

SOP checklist sign-off is currently frontend-only and is not persisted to the backend.

### 13.5 Database Schema Verification

Some application fields and mappings differ from the supplied SQL schema.

The live Supabase database must be checked before implementing RAG queries.

## 14. Glossary of FactoryOps Identifiers

| Identifier | Meaning |
|---|---|
| FAC-001 | Factory identifier |
| APX-01 | Factory code |
| M001–M024 | Machine identifiers |
| L01–L04 | Production line identifiers |
| ST-01–ST-06 | Station identifiers |
| PRD-* | Production record identifiers |
| MNT-* | Maintenance record identifiers |
| INC-* | Incident identifiers |
| WO-* | Work order identifiers |
| SOP-* | Standard Operating Procedure identifiers |
| T01–T08 | Technician identifiers appearing in historical datasets |

## 15. Purpose of This Document in Advanced RAG

This document provides the foundational knowledge required for the FactoryOps Advanced RAG Assistant.

It helps the assistant understand:

- What FactoryOps is.
- What the platform does.
- How the application is structured.
- What each module is responsible for.
- How manufacturing workflows operate.
- What data categories are available.
- How users interact with the system.
- Which capabilities are implemented and which are planned.

This document provides application-level context.

Detailed machine information, maintenance procedures, incident workflows, production calculations, work order rules, permissions, safety instructions, inventory and attendance rules are maintained in their respective knowledge documents.

## 16. Knowledge Accuracy Rules

The Advanced RAG Assistant must follow these rules when using this document:

1. Do not invent factory information.
2. Distinguish implemented features from planned enhancements.
3. Do not assume synthetic telemetry is real-time sensor data.
4. Use the operational database for current machine, production, maintenance, incident and work order information.
5. Do not assume that historical CSV records represent current operational state.
6. Follow the authenticated user's actual permissions.
7. Do not invent missing company policies or safety procedures.
8. When information is unavailable, clearly state that it is unavailable.
9. Use the relevant specialized knowledge documents for detailed operational questions.
10. Prefer verified application and database information over assumptions.

---

**Document:** 01_factoryops_overview.md  
**Project:** FactoryOps – AI Smart Factory Operations & Maintenance Platform  
**Knowledge Base:** FactoryOps Advanced RAG  
**Status:** Initial knowledge document – pending project-owner review