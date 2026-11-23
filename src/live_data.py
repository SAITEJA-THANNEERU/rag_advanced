from src.supabase_client import supabase
from src.permissions import authorize_table_access


# ============================================================
# 1. TABLE COLUMN ALLOWLIST
# ============================================================

TABLE_COLUMNS = {
    "machines": [
        "machine_id", "machine_name", "status", "health_score",
        "temperature_c", "vibration_mms", "pressure_bar",
        "speed_rpm", "oee", "factory_id"
    ],

    "production_records": [
        "production_id", "machine_id", "date", "shift",
        "planned_units", "actual_units", "good_units",
        "defect_units", "downtime_minutes",
        "actual_cycle_time_seconds", "oee_percent", "factory_id"
    ],

    "incidents": [
        "incident_id", "machine_id", "machine_name",
        "incident_type", "severity", "failure_category",
        "problem_description", "root_cause", "action_taken",
        "downtime_minutes", "defect_units", "technician_id",
        "technician_name", "status", "reported_at",
        "resolved_at", "factory_id"
    ],

    "maintenance_records": [
        "maintenance_id", "machine_id", "machine_name",
        "maintenance_type", "priority", "status",
        "technician_id", "technician_name", "failure_category",
        "problem_description", "root_cause", "action_taken",
        "start_time", "end_time", "duration_minutes",
        "downtime_minutes", "factory_id"
    ],

    "work_orders": [
        "work_order_id", "machine_id", "machine_name",
        "maintenance_id", "incident_id", "production_id",
        "work_order_type", "priority", "status",
        "technician_id", "technician_name", "failure_category",
        "problem_description", "root_cause", "action_taken",
        "start_time", "end_time", "duration_minutes",
        "downtime_minutes", "factory_id"
    ],

    "spare_parts": [
        "part_number", "name", "category", "stock_quantity",
        "min_reorder_level", "unit_cost_usd", "supplier",
        "location_bin", "machine_compatibility", "factory_id"
    ],

    "notifications": [
        "recipient_user_id", "recipient_role", "factory_id",
        "title", "message", "notification_type", "priority",
        "related_module", "related_record_id", "target_path",
        "is_read", "created_at"
    ],

    "data_quality_metrics": [
        "sensor_name", "machine_id", "uptime_percentage",
        "data_completeness_pct", "latency_ms",
        "anomalies_detected", "status", "last_sync", "factory_id"
    ],

    "sops": [
        "sop_id", "title", "machine_type", "category",
        "version", "last_updated", "author", "steps",
        "safety_precautions", "target_audience", "factory_id"
    ]
}


# ============================================================
# 2. FILTER ALLOWLIST
# ============================================================

ALLOWED_FILTERS = {
    "machines": [
        "machine_id", "status", "machine_name"
    ],

    "production_records": [
        "machine_id", "date", "shift"
    ],

    "incidents": [
        "incident_id", "machine_id", "status",
        "severity", "incident_type"
    ],

    "maintenance_records": [
        "maintenance_id", "machine_id", "status",
        "priority", "maintenance_type"
    ],

    "work_orders": [
        "work_order_id", "machine_id", "status",
        "priority", "work_order_type"
    ],

    "spare_parts": [
        "part_number", "category"
    ],

    "notifications": [
        "is_read", "priority", "notification_type"
    ],

    "data_quality_metrics": [
        "machine_id", "status", "sensor_name"
    ],

    "sops": [
        "sop_id", "category", "machine_type"
    ]
}


# ============================================================
# 3. STATUS DEFINITIONS
# ============================================================

OPEN_WORK_ORDER_STATUSES = [
    "Open",
    "Pending",
    "Pending Parts",
    "Scheduled",
    "In Progress"
]

UNRESOLVED_INCIDENT_STATUSES = [
    "Investigating"
]


# ============================================================
# 4. AUTHORIZED QUERY BUILDER
# ============================================================

def _validate_user(user, table):

    if not isinstance(user, dict):
        raise PermissionError("Invalid user context.")

    factory_id = authorize_table_access(user, table)

    role = user.get("role")
    user_id = user.get("user_id")

    if not isinstance(role, str):
        raise PermissionError("Invalid role.")

    if not isinstance(user_id, str) or not user_id.strip():
        raise PermissionError("Invalid user identity.")

    if factory_id is None and role != "SUPER_ADMIN":
        raise PermissionError("Factory assignment is required.")

    return factory_id, role, user_id


def _build_authorized_query(user, table, filters=None):

    if table not in TABLE_COLUMNS:
        raise ValueError(f"Table not allowed: {table}")

    filters = filters or {}

    if not isinstance(filters, dict):
        raise ValueError("Filters must be a dictionary.")

    for column, value in filters.items():

        if column not in ALLOWED_FILTERS.get(table, []):
            raise ValueError(
                f"Filtering by '{column}' is not allowed."
            )

        if isinstance(value, (list, tuple, set)) and not value:
            raise ValueError(
                f"Filter values for '{column}' cannot be empty."
            )

    factory_id, role, user_id = _validate_user(user, table)

    query = supabase.table(table).select(
        ",".join(TABLE_COLUMNS[table])
    )

    # Factory isolation
    if factory_id is not None:
        query = query.eq("factory_id", factory_id)

    # Technician restrictions
    if role == "TECHNICIAN":

        technician_tables = {
            "incidents",
            "maintenance_records",
            "work_orders",
            "machines",
            "notifications",
            "sops"
        }

        if table not in technician_tables:
            raise PermissionError(
                "Technicians cannot access this table."
            )

        if table in {
            "incidents",
            "maintenance_records",
            "work_orders"
        }:
            query = query.eq("technician_id", user_id)

        elif table == "notifications":
            query = query.eq("recipient_user_id", user_id)

    # Apply validated filters
    for column, value in filters.items():

        if isinstance(value, (list, tuple, set)):
            query = query.in_(column, list(value))
        else:
            query = query.eq(column, value)

    return query


def query_factory_table(
    user,
    table,
    filters=None,
    limit=100,
    offset=0
):
    """
    Fetch authorized records with pagination.

    Security:
    - Role-based table permissions.
    - Factory-level isolation.
    - Exact technician ID restrictions.
    - Allowlisted columns and filters.
    """

    try:
        limit = int(limit)
        offset = int(offset)
    except (TypeError, ValueError):
        raise ValueError("Invalid pagination values.")

    limit = max(1, min(limit, 1000))
    offset = max(0, offset)

    query = _build_authorized_query(
        user,
        table,
        filters
    )

    response = query.range(
        offset,
        offset + limit - 1
    ).execute()

    return response.data or []


# ============================================================
# 5. PAGINATED FULL DATA RETRIEVAL
# ============================================================

def get_all_authorized_records(
    user,
    table,
    filters=None,
    page_size=1000
):
    """
    Retrieve every accessible record using pagination.

    Factory and technician restrictions are applied
    independently to every page.
    """

    page_size = max(1, min(int(page_size), 1000))

    all_records = []
    offset = 0

    while True:

        page = query_factory_table(
            user=user,
            table=table,
            filters=filters,
            limit=page_size,
            offset=offset
        )

        all_records.extend(page)

        if len(page) < page_size:
            break

        offset += page_size

    return all_records


# ============================================================
# 6. MACHINE FUNCTIONS
# ============================================================

def get_machine_count(user):

    factory_id, _, _ = _validate_user(
        user,
        "machines"
    )

    query = supabase.table("machines").select(
        "machine_id",
        count="exact"
    )

    if factory_id is not None:
        query = query.eq("factory_id", factory_id)

    response = query.execute()

    return response.count or 0


def get_machine_details(user, machine_id):

    machine_id = str(machine_id).strip().upper()

    records = query_factory_table(
        user,
        "machines",
        filters={"machine_id": machine_id},
        limit=1
    )

    return records[0] if records else None


def get_all_machines(user, limit=100):

    return query_factory_table(
        user,
        "machines",
        limit=limit
    )


# ============================================================
# 7. PRODUCTION FUNCTIONS
# ============================================================

def get_production_records(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "production_records",
        filters=filters,
        limit=limit
    )


def _safe_number(value):

    if value is None:
        return 0

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0


def get_production_summary(user, filters=None):
    """
    Calculate totals using all authorized production records.

    This avoids presenting the first 100 records as
    the complete production history.
    """

    records = get_all_authorized_records(
        user,
        "production_records",
        filters=filters
    )

    fields = [
        "planned_units",
        "actual_units",
        "good_units",
        "defect_units",
        "downtime_minutes"
    ]

    summary = {
        "total_records": len(records)
    }

    for field in fields:

        summary[field] = sum(
            _safe_number(record.get(field))
            for record in records
        )

    summary["average_oee_percent"] = (
        round(
            sum(
                _safe_number(record.get("oee_percent"))
                for record in records
                if record.get("oee_percent") is not None
            )
            /
            sum(
                1 for record in records
                if record.get("oee_percent") is not None
            ),
            2
        )
        if any(
            record.get("oee_percent") is not None
            for record in records
        )
        else None
    )

    summary["average_cycle_time_seconds"] = (
        round(
            sum(
                _safe_number(
                    record.get("actual_cycle_time_seconds")
                )
                for record in records
                if record.get("actual_cycle_time_seconds") is not None
            )
            /
            sum(
                1 for record in records
                if record.get("actual_cycle_time_seconds") is not None
            ),
            2
        )
        if any(
            record.get("actual_cycle_time_seconds") is not None
            for record in records
        )
        else None
    )

    summary["data_scope"] = (
        "All records returned by paginated authorized database queries."
    )

    return summary


# ============================================================
# 8. INCIDENT FUNCTIONS
# ============================================================

def get_incidents(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "incidents",
        filters=filters,
        limit=limit
    )


def get_unresolved_incidents(user, limit=200):

    return query_factory_table(
        user,
        "incidents",
        filters={
            "status": UNRESOLVED_INCIDENT_STATUSES
        },
        limit=limit
    )


def get_unresolved_incident_count(user):

    records = get_all_authorized_records(
        user,
        "incidents",
        filters={
            "status": UNRESOLVED_INCIDENT_STATUSES
        }
    )

    return len(records)


# ============================================================
# 9. MAINTENANCE FUNCTIONS
# ============================================================

def get_maintenance_records(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "maintenance_records",
        filters=filters,
        limit=limit
    )


# ============================================================
# 10. WORK ORDER FUNCTIONS
# ============================================================

def get_work_orders(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "work_orders",
        filters=filters,
        limit=limit
    )


def get_open_work_orders(user, limit=200):

    return query_factory_table(
        user,
        "work_orders",
        filters={
            "status": OPEN_WORK_ORDER_STATUSES
        },
        limit=limit
    )


def get_all_open_work_orders(user):

    return get_all_authorized_records(
        user,
        "work_orders",
        filters={
            "status": OPEN_WORK_ORDER_STATUSES
        }
    )


def get_open_work_order_count(user):

    records = get_all_open_work_orders(user)

    return len(records)


# ============================================================
# 11. SPARE PART FUNCTIONS
# ============================================================

def get_spare_parts(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "spare_parts",
        filters=filters,
        limit=limit
    )


# ============================================================
# 12. NOTIFICATION FUNCTIONS
# ============================================================

def get_notifications(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "notifications",
        filters=filters,
        limit=limit
    )


# ============================================================
# 13. DATA QUALITY FUNCTIONS
# ============================================================

def get_data_quality_metrics(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "data_quality_metrics",
        filters=filters,
        limit=limit
    )


# ============================================================
# 14. SOP FUNCTIONS
# ============================================================

def get_sops(
    user,
    filters=None,
    limit=100
):

    return query_factory_table(
        user,
        "sops",
        filters=filters,
        limit=limit
    )
