
import json
import re

from src.config import retriever, llm

from langchain_core.runnables import RunnableLambda

from src.chains import (
    contextualize_chain,
    document_answer_chain,
    intent_chain,
    history_answer_chain,
    general_chain
)

from src.live_data import (
    get_machine_count,
    get_machine_details,
    get_all_machines,
    get_production_records,
    get_production_summary,
    get_incidents,
    get_unresolved_incidents,
    get_unresolved_incident_count,
    get_maintenance_records,
    get_work_orders,
    get_open_work_orders,
    get_all_open_work_orders,
    get_open_work_order_count,
    get_spare_parts,
    get_notifications,
    get_data_quality_metrics,
    get_sops,
    get_all_authorized_records
)


# ============================================================
# 1. DOCUMENT RETRIEVAL
# ============================================================

def retrieve_documents(inputs):

    standalone_question = contextualize_chain.invoke({
        "input": inputs["input"],
        "chat_history": inputs.get("chat_history", [])
    })

    print("\nRewritten Question:", standalone_question)

    documents = retriever.invoke(standalone_question)

    print("\nRetrieved Documents:", len(documents))

    if not documents:
        return (
            "I couldn't find relevant information in the "
            "FactoryOps knowledge base to answer this question."
        )

    context = "\n\n".join(
        f"""
Source: {doc.metadata.get('source', 'Unknown')}
Content:
{doc.page_content}
"""
        for doc in documents
    )

    return document_answer_chain.invoke({
        "input": standalone_question,
        "context": context
    })


# ============================================================
# 2. QUESTION HELPERS
# ============================================================

def extract_machine_id(question):

    match = re.search(
        r"\bm\d{3,}\b",
        question.lower()
    )

    return match.group(0).upper() if match else None


def is_count_question(question):

    terms = [
        "how many",
        "count",
        "number of",
        "total number",
        "total count",
        "how much"
    ]

    return any(term in question.lower() for term in terms)


def is_summary_question(question):

    terms = [
        "total",
        "overall",
        "summary",
        "summarize",
        "average",
        "average oee",
        "overall production"
    ]

    return any(term in question.lower() for term in terms)


# ============================================================
# 3. LIVE DATA TABLE DETECTION
# ============================================================

def detect_live_data_table(question):

    q = question.lower()

    # Explicit operational categories have priority.

    if any(term in q for term in [
        "work order",
        "work orders",
        "workorder",
        "workorders"
    ]):
        return "work_orders"

    if any(term in q for term in [
        "incident",
        "incidents",
        "failure",
        "failures"
    ]):
        return "incidents"

    if any(term in q for term in [
        "maintenance",
        "maintain",
        "servicing",
        "service records"
    ]):
        return "maintenance_records"

    if any(term in q for term in [
        "production",
        "produced",
        "output",
        "defects",
        "defective units",
        "downtime",
        "cycle time"
    ]):
        return "production_records"

    if any(term in q for term in [
        "spare part",
        "spare parts",
        "inventory",
        "stock",
        "reorder"
    ]):
        return "spare_parts"

    if any(term in q for term in [
        "notification",
        "notifications",
        "alerts"
    ]):
        return "notifications"

    if any(term in q for term in [
        "data quality",
        "sensor quality",
        "data completeness",
        "sensor metrics"
    ]):
        return "data_quality_metrics"

    if "sop" in q:
        return "sops"

    if any(term in q for term in [
        "machine",
        "machines",
        "equipment"
    ]) or extract_machine_id(q):

        return "machines"

    return None


# ============================================================
# 4. LIVE DATA RETRIEVAL
# ============================================================

def retrieve_live_data(inputs):

    question = inputs["input"]
    history = inputs.get("chat_history", [])
    user = inputs.get("user")

    if not user:
        return (
            "Unable to retrieve live data: "
            "authenticated user information is missing."
        )

    standalone_question = contextualize_chain.invoke({
        "input": question,
        "chat_history": history
    })

    question_lower = standalone_question.lower()

    print("\nLive Data Question:", standalone_question)

    try:

        selected_table = detect_live_data_table(
            standalone_question
        )

        machine_id = extract_machine_id(
            standalone_question
        )

        print("\nSelected Table:", selected_table)
        print("Machine ID:", machine_id)

        if selected_table is None:
            return (
                "I couldn't identify the FactoryOps operational "
                "data required for this question."
            )

        data = None

        # ----------------------------------------------------
        # MACHINES
        # ----------------------------------------------------

        if selected_table == "machines":

            if machine_id:

                data = get_machine_details(
                    user,
                    machine_id
                )

            elif is_count_question(question_lower):

                data = {
                    "total_machines": get_machine_count(user)
                }

            else:

                data = get_all_machines(user)

        # ----------------------------------------------------
        # PRODUCTION
        # ----------------------------------------------------

        elif selected_table == "production_records":

            filters = {}

            if machine_id:
                filters["machine_id"] = machine_id

            if is_summary_question(question_lower) or is_count_question(
                question_lower
            ):

                data = get_production_summary(
                    user,
                    filters=filters or None
                )

            else:

                data = get_production_records(
                    user,
                    filters=filters or None,
                    limit=100
                )

        # ----------------------------------------------------
        # INCIDENTS
        # ----------------------------------------------------

        elif selected_table == "incidents":

            if any(term in question_lower for term in [
                "unresolved",
                "unresolved incidents",
                "investigating",
                "not resolved",
                "still open"
            ]):

                if is_count_question(question_lower):

                    data = {
                        "unresolved_incident_count":
                            get_unresolved_incident_count(user)
                    }

                else:

                    data = get_all_authorized_records(
                        user,
                        "incidents",
                        filters={"status": ["Investigating"]}
                    )

            elif is_count_question(question_lower):

                records = get_all_authorized_records(
                    user,
                    "incidents"
                )

                data = {
                    "total_incidents": len(records)
                }

            else:

                data = get_incidents(
                    user,
                    limit=100
                )

        # ----------------------------------------------------
        # MAINTENANCE
        # ----------------------------------------------------

        elif selected_table == "maintenance_records":

            if is_count_question(question_lower):

                records = get_all_authorized_records(
                    user,
                    "maintenance_records"
                )

                data = {
                    "total_maintenance_records": len(records)
                }

            else:

                data = get_maintenance_records(
                    user,
                    limit=100
                )

        # ----------------------------------------------------
        # WORK ORDERS
        # ----------------------------------------------------

        elif selected_table == "work_orders":

            if any(term in question_lower for term in [
                "open",
                "pending",
                "outstanding",
                "in progress",
                "active work"
            ]):

                if is_count_question(question_lower):

                    data = {
                        "open_work_order_count":
                            get_open_work_order_count(user)
                    }

                else:

                    data = get_all_open_work_orders(user)

            elif is_count_question(question_lower):

                records = get_all_authorized_records(
                    user,
                    "work_orders"
                )

                data = {
                    "total_work_orders": len(records)
                }

            else:

                data = get_work_orders(
                    user,
                    limit=100
                )

        # ----------------------------------------------------
        # SPARE PARTS
        # ----------------------------------------------------

        elif selected_table == "spare_parts":

            data = get_spare_parts(
                user,
                limit=100
            )

        # ----------------------------------------------------
        # NOTIFICATIONS
        # ----------------------------------------------------

        elif selected_table == "notifications":

            data = get_notifications(
                user,
                limit=100
            )

        # ----------------------------------------------------
        # DATA QUALITY
        # ----------------------------------------------------

        elif selected_table == "data_quality_metrics":

            data = get_data_quality_metrics(
                user,
                limit=100
            )

        # ----------------------------------------------------
        # SOP RECORDS
        # ----------------------------------------------------

        elif selected_table == "sops":

            data = get_sops(
                user,
                limit=100
            )

        # ----------------------------------------------------
        # EMPTY DATA HANDLING
        # ----------------------------------------------------

        if data is None or data == []:

            return "No matching live records were found."

        # ----------------------------------------------------
        # LLM ANSWER GENERATION
        # ----------------------------------------------------

        live_data_prompt = f"""
You are the FactoryOps live operational data assistant.

Answer the user's question using ONLY the database
information supplied below.

IMPORTANT RULES:

1. Never invent database values or records.
2. Never use static document information as current data.
3. Preserve machine IDs and numerical values.
4. Do not change database status values.
5. Clearly distinguish Open, Pending, Pending Parts,
   Scheduled, In Progress and Completed.
6. Do not describe completed work orders as open.
7. Do not describe investigating incidents as closed.
8. Do not claim that retrieved records represent the
   entire database unless the supplied data confirms it.
9. For production summaries, use the supplied calculated
   totals rather than recalculating from sample records.
10. If information is unavailable, say so clearly.
11. Never reveal information outside the authenticated
    user's authorized factory or technician scope.

Selected Database Table:
{selected_table}

User Question:
{standalone_question}

Database Information:
{json.dumps(data, default=str, indent=2)}

Provide a clear, accurate and professional answer.
"""

        response = llm.invoke(live_data_prompt)

        return response.content

    except PermissionError:

        print("Live data access denied.")

        return (
            "You don't have permission to access "
            "this operational information."
        )

    except Exception as e:

        print("Live data retrieval error:", str(e))

        return (
            "Unable to retrieve live FactoryOps data "
            "at the moment."
        )


# ============================================================
# 5. MAIN QUERY ROUTER
# ============================================================

def route_request(inputs):

    question = inputs["input"]
    history = inputs.get("chat_history", [])

    intent = intent_chain.invoke({
        "input": question,
        "chat_history": history
    }).strip().upper()

    print("\nDetected Intent:", intent)

    if intent == "DOCUMENT":

        return retrieve_documents({
            "input": question,
            "chat_history": history
        })

    elif intent == "LIVE_DATA":

        return retrieve_live_data({
            "input": question,
            "chat_history": history,
            "user": inputs.get("user")
        })

    elif intent == "HISTORY":

        return history_answer_chain.invoke({
            "input": question,
            "chat_history": history
        })

    elif intent == "GENERAL":

        return general_chain.invoke({
            "input": question,
            "chat_history": history
        })

    else:

        print("Unknown intent. Using general chain.")

        return general_chain.invoke({
            "input": question,
            "chat_history": history
        })


# ============================================================
# 6. RAG CHAIN
# ============================================================

rag_chain = RunnableLambda(route_request)