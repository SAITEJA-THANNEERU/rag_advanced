# ==========================================
# FACTORYOPS ROLE-BASED ACCESS CONTROL
# ==========================================

ROLE_PERMISSIONS = {

    "SUPER_ADMIN": {
        "machines",
        "production_records",
        "incidents",
        "maintenance_records",
        "work_orders",
        "spare_parts",
        "notifications",
        "data_quality_metrics",
        "system_audit_logs",
        "sops"
    },

    "ADMIN": {
        "machines",
        "production_records",
        "incidents",
        "maintenance_records",
        "work_orders",
        "spare_parts",
        "notifications",
        "data_quality_metrics",
        "system_audit_logs",
        "sops"
    },

    "MANAGER_SUPERVISOR": {
        "machines",
        "production_records",
        "incidents",
        "maintenance_records",
        "work_orders",
        "spare_parts",
        "notifications",
        "system_audit_logs",
        "sops"
    },

    "PRODUCTION_PLANNER": {
        "machines",
        "production_records",
        "incidents",
        "maintenance_records",
        "work_orders",
        "notifications",
        "sops"
    },

    "TECHNICIAN": {
        "machines",
        "incidents",
        "maintenance_records",
        "work_orders",
        "notifications",
        "sops"
    }
}


def can_access_table(role: str, table: str) -> bool:
    """
    Check whether a role can access an operational table.
    """

    allowed_tables = ROLE_PERMISSIONS.get(role)

    if allowed_tables is None:
        return False

    return table in allowed_tables


def get_authorized_factory_id(user: dict):
    """
    Return the authenticated user's factory ID.

    SUPER_ADMIN may have no factory assignment.
    Other roles must have a factory assignment.
    """

    role = user.get("role")
    factory_id = user.get("factory_id")

    if role not in ROLE_PERMISSIONS:
        raise PermissionError("Unauthorized user role")

    if role == "SUPER_ADMIN":
        return factory_id

    if not factory_id:
        raise PermissionError("Factory assignment required")

    return factory_id


def authorize_table_access(user: dict, table: str):
    """
    Validate role permission and factory assignment.
    """

    role = user.get("role")

    if not can_access_table(role, table):
        raise PermissionError(
            f"Role {role} cannot access {table}"
        )

    return get_authorized_factory_id(user)
