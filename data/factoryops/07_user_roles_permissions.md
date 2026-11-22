# FactoryOps — User Roles and Permissions

## 1. Purpose

This document defines the user roles, access permissions, and authorization rules implemented in FactoryOps.

FactoryOps uses Role-Based Access Control (RBAC) to control:

- Dashboard access
- Module visibility
- Data access
- Operational record creation
- Record updates and deletion
- Technician assignments
- Work-order management
- Attendance management
- Inventory management
- Administrative operations

The RAG assistant must follow the same permission boundaries as the FactoryOps application.

A user must only receive information and assistance permitted by their authenticated role.

---

## 2. Authentication and Authorization Architecture

FactoryOps implements authentication and authorization through its React frontend and Express backend.

### Frontend authorization

File:

`src/utils/rbac.ts`

The frontend uses the `ROLE_PERMISSIONS` configuration to control:

- Navigation links
- Route access
- Button visibility
- Module access
- Role-specific UI behavior

The route authorization helper is:

`isRouteAllowedForRole`

### Backend authorization

File:

`server.ts`

The backend uses authentication and role authorization middleware:

- `authenticate`
- `authorizeRole(...roles)`

Backend authorization controls access to protected API endpoints.

### Critical security rule

Frontend restrictions are not sufficient for security.

The backend must independently validate the authenticated user and their permissions.

The RAG assistant must never trust a role supplied directly by the frontend or included in a user message.

---

## 3. Active User Roles

FactoryOps currently defines five primary roles.

| Role | General Responsibility |
|---|---|
| SUPER_ADMIN | System-wide administration and oversight. |
| ADMIN | Factory administration and operational control. |
| MANAGER_SUPERVISOR | Factory operations and workforce supervision. |
| PRODUCTION_PLANNER | Production planning and operational analysis. |
| TECHNICIAN | Assigned maintenance, repair, and operational activities. |

Each role has different permissions.

---

## 4. Legacy Role Aliases

FactoryOps supports legacy role names that map to the current roles.

| Legacy Role | Current Role |
|---|---|
| FACTORY_OWNER | ADMIN |
| FACTORY_MANAGER | MANAGER_SUPERVISOR |
| SUPERVISOR | MANAGER_SUPERVISOR |
| ANALYST | PRODUCTION_PLANNER |
| OPERATOR | TECHNICIAN |

These aliases are mapped in the `ROLE_PERMISSIONS` configuration.

The assistant should recognize the aliases when interpreting existing user records.

---

## 5. Route Access Matrix

The following routes are available according to the inspected frontend RBAC configuration.

| Route | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| `/dashboard` | Yes | Yes | Yes | Yes | Yes |
| `/attendance` | Yes | Yes | Yes | Yes | Yes |
| `/inventory` | Yes | Yes | Yes | Yes | Yes |
| `/production` | Yes | Yes | Yes | Yes | No |
| `/machines` | Yes | Yes | Yes | Yes | Yes |
| `/maintenance` | Yes | Yes | No | No | Yes |
| `/incidents` | Yes | Yes | Yes | No | Yes |
| `/work-orders` | Yes | Yes | Yes | Yes | Yes |
| `/quality` | Yes | Yes | Yes | No | No |
| `/analytics` | Yes | No | No | Yes | No |
| `/sops` | Yes | Yes | Yes | No | Yes |
| `/data-quality` | Yes | Yes | No | No | No |
| `/admin` | Yes | Yes | No | No | No |
| `/super-admin/*` | Yes | No | No | No | No |
| `/assigned-tasks` | No | No | No | No | Yes |
| `/my-assigned-tasks` | No | No | No | No | Yes |
| `/my-attendance` | No | No | No | No | Yes |

### Important route discrepancy

The Manager/Supervisor role has maintenance logging permission in the permission configuration, but `/maintenance` is missing from its allowed route list.

This is a frontend route-configuration inconsistency.

The assistant must not assume that API permission automatically means frontend route access.

---

## 6. Dashboard Permissions

| Role | Dashboard |
|---|---|
| SUPER_ADMIN | Executive Overview with read-only observer tabs for operational roles. |
| ADMIN | Admin Operations Dashboard. |
| MANAGER_SUPERVISOR | Factory Manager Dashboard with assignment and verification features. |
| PRODUCTION_PLANNER | Production Planner Dashboard. |
| TECHNICIAN | Technician Console. |

### SUPER_ADMIN Dashboard

Provides:

- Executive overview
- Plant-level operational visibility
- Role-specific observer views
- Workforce and operational monitoring

### ADMIN Dashboard

Provides:

- Factory operational KPIs
- Machine and production monitoring
- Incident visibility
- Work-order queue
- Defect-rate information

### MANAGER_SUPERVISOR Dashboard

Provides:

- Factory operational monitoring
- Incident and work-order management
- Technician assignment recommendations
- Assignment review
- Repair verification

### PRODUCTION_PLANNER Dashboard

Provides:

- Production planning
- Planned versus actual output
- Production shortfall
- Machine and shift analysis
- Scheduling information

### TECHNICIAN Dashboard

Provides:

- Technician profile information
- Assigned work
- Maintenance-related information
- Open incident visibility
- Failure-category information
- Downtime and work-order charts

---

## 7. Machine Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View machines | Yes | Yes | Yes | Yes | Yes |
| Create machines | Yes | Yes | Yes | No | No |
| Edit machines | Yes | Yes | Yes | No | No |
| Update machine status | Yes | Yes | Yes | No | Yes |
| Configure thresholds | Yes | Yes | Yes | No | No |
| Delete machines | Yes | Yes | No | No | No |

Technicians have limited machine access.

They can view machines and update machine status but cannot perform full machine administration.

---

## 8. Production Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View production | Yes | Yes | Yes | Yes | No route |
| Log production | Yes | Yes | Yes | Yes | No |
| Delete production | Yes | Yes | No | No | No |

Production Planner users can log production but cannot delete production records.

---

## 9. Maintenance Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View maintenance | Yes | Yes | Not available through route | Read-only | Yes |
| Log maintenance | Yes | Yes | API allowed | No | Yes |
| Delete maintenance | Yes | Yes | No | No | No |

### Important limitation

Manager/Supervisor maintenance access has a route mismatch:

- The API allows maintenance logging.
- The frontend allowed-route configuration omits `/maintenance`.

The assistant must distinguish backend permissions from frontend navigation access.

---

## 10. Incident Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| Report incidents | Yes | Yes | Yes | No | Yes |
| Update incidents | Yes | Yes | Yes | No | Yes |
| Delete incidents | Yes | Yes | No | No | No |
| View incidents | Yes | Yes | Yes | No route | Yes |

Technicians can report incidents and update permitted incident information.

Managers and administrators have broader incident-management permissions.

---

## 11. Work Order Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View work orders | Yes | Yes | Yes | Yes | Yes |
| Create work orders | Yes | Yes | Yes | No | No |
| Update work orders | Yes | Yes | Yes | No | Assigned only |
| Complete work orders | Yes | Yes | Yes | No | No |
| Delete work orders | Yes | Yes | Yes | No | No |

### Backend restrictions

The backend enforces the following rules:

- TECHNICIAN cannot create work orders.
- PRODUCTION_PLANNER cannot create work orders.
- TECHNICIAN cannot directly set a work order to `Completed`.
- Only authorized administrative and management roles can delete work orders.

Unauthorized creation or completion attempts can return HTTP 403.

### Frontend/backend mismatch

Some frontend components display work-order creation buttons for Technicians and Production Planners.

However, the backend rejects their creation requests.

Backend authorization is authoritative.

---

## 12. Technician Assignment Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View all assignments | Yes | Yes | Yes | Restricted | No |
| Recommend technicians | Authorized | Authorized | Yes | No | No |
| Dispatch assignments | Yes | Yes | Yes | No | No |
| Verify repairs | Authorized | Yes, subject to self-repair rule | Yes, subject to self-repair rule | No | No |
| Review reassignment requests | Authorized | Authorized | Yes | No | No |
| View own assignments | Yes | Yes | Yes | Restricted | Yes |
| Accept assignment | No | No | No | No | Yes |
| Reject assignment | No | No | No | No | Yes |
| Request reassignment | No | No | No | No | Yes |
| Start repair | No | No | No | No | Yes |
| Submit progress | No | No | No | No | Yes |
| Submit resolution | No | No | No | No | Yes |

### Technician restrictions

Technicians can:

- View their own assignments.
- Accept assignments.
- Reject assignments with a reason.
- Request reassignment with a reason.
- Start repair work.
- Submit progress updates.
- Submit repair resolutions.

Technicians cannot verify their own repairs.

### Self-verification rule

A user cannot verify a repair when `isSelfRepair === true`, except for `SUPER_ADMIN`.

This restriction is enforced by the backend.

---

## 13. Assignment Information Redaction

Production Planners have restricted access to technician assignment information.

The following fields are redacted:

- `rejection_reason`
- `reassignment_reason`

This prevents Production Planners from viewing restricted assignment explanations.

### RAG instruction

The assistant must apply the same redaction rules when retrieving assignment information.

It must never expose restricted reasons through natural-language answers, summaries, or generated reports.

Technicians must only receive their own assignment information.

---

## 14. Spare Parts Inventory Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View inventory | Yes | Yes | Yes | Yes | Yes |
| Create inventory items | Yes | Yes | Yes | No | No |
| Edit inventory items | Yes | Yes | Yes | No | Yes |
| Restock inventory | Yes | Yes | Yes | No | Yes |
| Delete inventory items | Yes | Yes | Yes | No | No |

Production Planners have read-only inventory access.

Technicians can edit and restock inventory but cannot delete inventory items.

---

## 15. Attendance and Geofencing Permissions

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View all attendance | Yes | Yes | Team technicians | No | No |
| Configure geofence | Yes | Yes | No | No | No |
| Own check-in | Yes | Yes | Yes | Yes | Yes |
| Report absence | Yes | Yes | Yes | Yes | Yes |

Manager/Supervisor users can view attendance information for their technician team.

Production Planners and Technicians have access to their own attendance and absence-reporting functionality.

---

## 16. User Administration, Cloud Sync, and Audit Logs

### SUPER_ADMIN

Has full access to:

- User management
- Cloud synchronization
- Audit logs
- Administrative configuration

### ADMIN

Has full access to:

- User management
- Cloud synchronization
- Audit logs
- Factory administration

### MANAGER_SUPERVISOR

Can:

- View audit logs.

Cannot:

- Perform user CRUD.
- Configure the GPS geofence.
- Access all administrative operations.

### PRODUCTION_PLANNER

Has restricted administrative access.

### TECHNICIAN

Does not have general administrative access.

The assistant must not expose user-management or audit information to roles that do not have permission.

---

## 17. Registration Restrictions

The public registration endpoint is:

`POST /api/auth/register`

Public registration permits these roles:

- MANAGER_SUPERVISOR
- TECHNICIAN
- PRODUCTION_PLANNER

Public registration does not permit:

- ADMIN
- SUPER_ADMIN

Attempts to register restricted roles return HTTP 403.

Other verified registration rules:

- Minimum password length: 8 characters.
- Duplicate email: HTTP 409.

Administrative roles must be provisioned through an authorized administrative process.

---

## 18. RAG Assistant Authorization Rules

The RAG assistant is an application component and must follow the authenticated user's FactoryOps permissions.

### Rule 1: Trust the authenticated identity

Retrieve the user's identity and role from the verified backend authentication context.

Never trust a role supplied in the question or request body.

### Rule 2: Enforce permissions on the backend

All operational data tools must enforce role permissions before returning results.

### Rule 3: Restrict technician data

Technicians must only retrieve their own assignment information.

### Rule 4: Redact restricted assignment reasons

Production Planners must not receive:

- Rejection reasons.
- Reassignment reasons.

### Rule 5: Restrict work-order actions

The assistant must not offer unauthorized work-order creation, completion, or deletion actions.

### Rule 6: Restrict administrative information

User management, audit logs, and configuration information must remain limited to authorized roles.

### Rule 7: Filter by factory

Operational queries must respect the authenticated user's factory scope.

The current application enforces single-factory operational access for FAC-001.

### Rule 8: Do not confuse visibility with modification permission

A user who can view a record does not automatically have permission to edit, delete, or approve it.

---

## 19. Recommended RAG Data Retrieval Strategy

The RAG integration should receive an authenticated context containing:

- User ID
- Verified role
- Factory ID
- Relevant permission scope

The context must originate from the backend authentication process.

### Example: Technician query

Question:

"Show my assigned repair tasks."

Expected behavior:

1. Authenticate the user.
2. Retrieve the verified technician identity.
3. Query only assignments belonging to that technician.
4. Return permitted assignment fields.
5. Do not expose other technicians' private assignments.

### Example: Production Planner query

Question:

"Show technician reassignment requests."

Expected behavior:

1. Authenticate the Production Planner.
2. Retrieve permitted assignment information.
3. Redact rejection and reassignment reasons.
4. Return only authorized fields.

### Example: Technician work-order query

Question:

"Complete work order WO-2026-0001."

Expected behavior:

1. Authenticate the technician.
2. Check the user's permissions.
3. Reject the completion action.
4. Explain that manager or administrator authorization is required.

The assistant must not bypass backend authorization through LLM-generated actions.

---

## 20. Important Implementation Gaps

The inspected application contains several frontend/backend inconsistencies:

1. Manager/Supervisor has maintenance logging API permission, but the `/maintenance` route is missing from the frontend allowed-route configuration.
2. Technician Dashboard displays a maintenance button connected to work-order creation, but the backend rejects technician work-order creation.
3. Production Planner Dashboard displays work-order creation buttons, but the backend rejects Production Planner work-order creation.

These inconsistencies should be addressed in the application.

The RAG assistant must follow backend authorization even when the frontend displays an action that the backend does not permit.

---

## 21. Security and Accuracy Rules

The RAG assistant must follow these rules:

1. Never trust frontend-supplied roles.
2. Never trust user-written claims of administrative privileges.
3. Always validate the authenticated user on the backend.
4. Enforce role permissions for every operational data tool.
5. Restrict technicians to their own assignments.
6. Redact reassignment and rejection reasons for Production Planners.
7. Prevent technicians from verifying their own repairs.
8. Prevent technicians from directly completing work orders.
9. Prevent Technicians and Production Planners from creating work orders.
10. Never expose administrative information to unauthorized users.
11. Respect factory-level data scope.
12. Distinguish read permissions from write permissions.
13. Treat backend authorization as authoritative over frontend visibility.

---

## 22. Summary

FactoryOps implements five primary roles:

- SUPER_ADMIN
- ADMIN
- MANAGER_SUPERVISOR
- PRODUCTION_PLANNER
- TECHNICIAN

Each role has different access to dashboards, machines, production, maintenance, incidents, work orders, technician assignments, inventory, attendance, and administration.

The application uses frontend route restrictions and backend authorization middleware.

For the RAG integration, backend authorization must remain the final security boundary. The assistant must retrieve only permitted information, respect assignment ownership, apply field-level redaction, and never execute actions beyond the authenticated user's permissions.