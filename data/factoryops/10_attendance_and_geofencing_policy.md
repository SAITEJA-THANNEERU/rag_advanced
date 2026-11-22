# FactoryOps — Attendance and Geofencing Policy

## 1. Purpose

FactoryOps includes an Attendance and Geofencing module to manage employee attendance and verify whether check-ins occur within the configured factory location.

The module supports:

- GPS-based attendance check-in.
- Factory geofence validation.
- Employee attendance records.
- Absence reporting.
- Duplicate check-in prevention.
- Manager attendance monitoring.
- Administrator attendance monitoring.
- Attendance audit information.

The system uses geographical distance validation to determine whether a user's check-in location is within the permitted factory radius.

---

## 2. Attendance Module Overview

### Frontend components

- `AttendanceHubPage.tsx`
- `MyAttendancePage.tsx`
- `ManagerAttendancePage.tsx`
- `AdminAttendancePage.tsx`

### Backend endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/attendance/factory-location` | Retrieve factory location configuration. |
| POST | `/api/attendance/factory-location` | Configure factory location. |
| POST | `/api/attendance/check-in` | Submit attendance check-in. |
| POST | `/api/attendance/report-absence` | Report an absence. |
| GET | `/api/attendance/my` | Retrieve personal attendance. |
| GET | `/api/attendance/manager` | Retrieve manager-level attendance information. |
| GET | `/api/attendance/admin` | Retrieve administrative attendance information. |

The backend performs attendance validation and enforces access restrictions.

---

## 3. Factory Geofence Configuration

FactoryOps uses GPS coordinates to define the factory location.

### Default factory location

| Property | Value |
|---|---|
| Factory | Apex Precision Manufacturing |
| Factory ID | FAC-001 |
| Location | Hyderabad, Telangana |
| Latitude | 17.4435 |
| Longitude | 78.3772 |
| Geofence radius | 1,000 metres |
| Equivalent distance | 1 kilometre |

The configured location can be managed through the factory attendance configuration functionality.

The default coordinates should not be assumed to represent the currently configured live coordinates without checking the application.

---

## 4. GPS Geofence Validation

FactoryOps uses the Haversine distance calculation to determine the geographical distance between the employee's submitted GPS coordinates and the configured factory location.

### Validation rule

The permitted geofence radius is:

```text
1000 metres
```

The backend compares the calculated distance with the configured factory radius.

A check-in must satisfy the geofence validation.

### Haversine formula

The Haversine formula calculates the great-circle distance between two geographical coordinates.

```text
a = sin²(Δlat / 2)
    + cos(lat1) × cos(lat2) × sin²(Δlon / 2)

c = 2 × atan2(√a, √(1-a))

distance = R × c
```

Where:

- `lat1` and `lon1` represent the factory coordinates.
- `lat2` and `lon2` represent the employee's submitted coordinates.
- `R` represents Earth's mean radius.
- `distance` represents the calculated geographical distance.

### Important rule

The backend performs the distance validation.

The frontend must not be treated as the final authority for determining whether a check-in is valid.

---

## 5. Attendance Check-In

Employees can submit attendance through the attendance interface.

The backend validates the submitted attendance information.

### General workflow

1. The employee opens the attendance interface.
2. The application obtains the employee's GPS location.
3. The employee submits a check-in request.
4. The backend calculates the distance from the configured factory location.
5. The backend validates the 1,000-metre geofence.
6. The attendance record is processed according to the application's validation rules.

### Duplicate check-in prevention

FactoryOps permits only one attendance record per user per calendar date.

If a user attempts to create another attendance record for the same date, the backend rejects the duplicate request.

The response is:

```text
HTTP 409 Conflict
```

---

## 6. Attendance Status and Validation

FactoryOps includes attendance records and absence-reporting functionality.

### Verified attendance rules

| Rule | Behavior |
|---|---|
| Geofence | 1,000-metre Haversine validation. |
| Duplicate attendance | One record per user per calendar date. |
| Duplicate request | HTTP 409 Conflict. |
| Verified Present record | Cannot be overwritten by a self-reported absence. |
| On-time cutoff | Check-in time less than or equal to 08:30:00. |

### On-time classification

The verified cutoff is:

```text
08:30:00
```

A check-in at or before this time satisfies the configured on-time cutoff.

A check-in after this time does not satisfy the cutoff.

**Important:** The cutoff is a verified application rule. The complete official shift and grace-period policy has not been verified.

---

## 7. Absence Reporting

FactoryOps supports employee absence reporting.

The following absence reasons are accepted:

| Absence Reason |
|---|
| Sick Leave |
| Emergency |
| Casual Leave |
| Off-Site Duty |
| Other |

### Absence reporting workflow

1. The employee opens the attendance interface.
2. The employee selects the absence-reporting option.
3. The employee selects an available absence reason.
4. The employee submits the absence request.
5. The backend validates the request.
6. The attendance information is processed.

### Important restriction

A verified `Present` attendance record cannot be overwritten by a self-reported absence.

The assistant must not suggest that users can replace an already verified Present record by submitting an absence report.

---

## 8. Attendance Permissions by Role

FactoryOps uses role-based access control for attendance operations.

| Action | SUPER_ADMIN | ADMIN | MANAGER_SUPERVISOR | PRODUCTION_PLANNER | TECHNICIAN |
|---|---|---|---|---|---|
| View all attendance | Yes | Yes | Team technicians | No | No |
| Configure geofence | Yes | Yes | No | No | No |
| Own check-in | Yes | Yes | Yes | Yes | Yes |
| Report absence | Yes | Yes | Yes | Yes | Yes |
| View own attendance | Yes | Yes | Yes | Yes | Yes |

### SUPER_ADMIN

Can:

- View attendance information.
- Configure the factory geofence.
- Access administrative attendance functionality.

### ADMIN

Can:

- View attendance information.
- Configure the factory geofence.
- Access administrative attendance functionality.

### MANAGER_SUPERVISOR

Can:

- Check in.
- Report an absence.
- View attendance information for team technicians.

Cannot configure the factory geofence.

### PRODUCTION_PLANNER

Can:

- Check in.
- Report an absence.
- View personal attendance information.

Cannot access general attendance administration.

### TECHNICIAN

Can:

- Check in.
- Report an absence.
- View personal attendance information.

Cannot access general attendance administration.

---

## 9. Attendance Audit Information

FactoryOps includes attendance-related audit functionality.

The application records attendance-related information through its attendance and audit workflows.

However, the inspected source identifies the following persistence limitation:

- `factory_locations` and `attendance_audit_logs` are stored in local JSON or in-memory application state.
- They are not defined in the inspected Supabase SQL schema.
- `attendance_records` is referenced in the RLS configuration, but its DDL is missing.
- Attendance records are not synced by the inspected `server.ts` Supabase synchronization implementation.

Therefore, the RAG assistant must not assume that all attendance information is permanently stored in Supabase.

The actual current persistence source should be checked before answering questions about historical attendance availability.

---

## 10. Shift Timings and Attendance Policy Gaps

The application contains a verified on-time cutoff of 08:30:00.

However, the complete official shift schedule has not been established.

The following information remains missing or requires authorized approval:

| Area | Status |
|---|---|
| Official Shift A timing | Requires confirmation |
| Official Shift B timing | Requires confirmation |
| Official Shift C timing | Requires confirmation |
| Attendance grace period | Missing |
| Late-arrival approval rules | Missing |
| Leave approval workflow | Missing |
| Leave balance and annual entitlement | Missing |
| Holiday calendar | Missing |
| Overtime policy | Missing |
| Attendance correction procedure | Missing |

A Morning shift fallback of 06:00–14:00 appears in `TechnicianDashboardView`, but this does not establish the complete official shift schedule.

The assistant must not treat that fallback as the approved timing for every employee.

---

## 11. Recommended RAG Integration

Attendance questions often require current structured data rather than vector-document retrieval alone.

Recommended query types include:

### Personal attendance

Example:

"Show my attendance records."

Expected behavior:

1. Authenticate the user.
2. Retrieve the verified user identity.
3. Query only that user's attendance records.
4. Return the available attendance information.

### Team attendance

Example:

"Show my technicians' attendance."

Expected behavior:

1. Authenticate the Manager/Supervisor.
2. Verify team attendance permissions.
3. Retrieve attendance records within the permitted team scope.
4. Return the permitted information.

### Geofence question

Example:

"What is the FactoryOps attendance geofence radius?"

Expected answer:

"The configured attendance geofence uses a 1,000-metre radius and Haversine distance validation."

### On-time question

Example:

"What is the attendance on-time cutoff?"

Expected answer:

"The verified application cutoff is 08:30:00. The complete official shift and grace-period policy has not been confirmed."

---

## 12. RAG Security Requirements

The RAG assistant must follow these rules:

1. Retrieve attendance information using the authenticated user's identity.
2. Never trust a user-provided employee ID as authorization.
3. Restrict employees to their own attendance information.
4. Allow Managers/Supervisors only their permitted team attendance information.
5. Restrict administrative attendance access to authorized roles.
6. Do not allow unauthorized geofence configuration.
7. Respect duplicate check-in prevention.
8. Do not claim that a verified Present record can be overwritten by self-reported absence.
9. Use current structured records for attendance queries.
10. Clearly identify missing attendance information.

Attendance information must not be exposed across unauthorized users or teams.

---

## 13. Important Implementation Limitations

The following points must be considered during RAG integration:

1. Attendance uses custom Express authentication and backend authorization.
2. The geofence validation is implemented in the backend.
3. The configured radius is 1,000 metres.
4. Only one attendance record per user per calendar date is permitted.
5. The on-time cutoff is 08:30:00.
6. Absence reporting supports five verified reasons.
7. The complete HR leave policy is not available.
8. Official A/B/C shift timings are not fully confirmed.
9. The attendance-related Supabase schema is incomplete in the inspected SQL files.
10. Attendance synchronization with Supabase is not implemented in the inspected backend synchronization code.

---

## 14. Summary

FactoryOps provides GPS-based attendance management using Haversine distance validation.

The verified rules include:

- A 1,000-metre geofence.
- One attendance record per user per calendar date.
- HTTP 409 for duplicate attendance requests.
- An on-time cutoff of 08:30:00.
- Five accepted absence reasons.
- Protection against overwriting a verified Present record with a self-reported absence.

SUPER_ADMIN and ADMIN have attendance administration and geofence configuration permissions. Managers can view team technician attendance, while Production Planners and Technicians have personal attendance access.

The Advanced RAG assistant must respect these access restrictions and clearly distinguish verified application behavior from missing HR policies.