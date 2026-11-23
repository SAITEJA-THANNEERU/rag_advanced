from src.supabase_client import supabase


def get_machine_count():
    """Get the current number of registered machines."""

    response = (
        supabase.table("machines")
        .select("machine_id", count="exact")
        .execute()
    )

    return response.count or 0


def get_machine_details(machine_id):
    """Fetch live details of a specific machine."""

    response = (
        supabase.table("machines")
        .select("*")
        .eq("machine_id", machine_id.upper())
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


def get_all_machines():
    """Fetch all registered machines."""

    response = (
        supabase.table("machines")
        .select("*")
        .execute()
    )

    return response.data or []