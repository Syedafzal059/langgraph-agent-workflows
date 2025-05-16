from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict, Literal
from langgraph_email_approval.email_tool import send_approval_email
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

#checkpointer = SqliteSaver("./graph.db")


class State(TypedDict):
    topic: str
    document: str
    thread_id: str

def generate_doc(state: State) -> dict:
    return {"document": f" {state['topic']} is transforming healthcare by enhancing diagnostics, personalizing treatments, and improving operational efficiency. AI algorithms can analyze medical images with high accuracy, detect early signs of disease, and assist in clinical decision-making. In personalized medicine, AI uses patient data to tailor treatments, improving outcomes. It also powers virtual health assistants, streamlines hospital workflows, and supports drug discovery. By automating repetitive tasks, AI frees up time for healthcare professionals to focus on patient care. While challenges like data privacy and ethical considerations remain, AI holds immense promise to make healthcare more predictive, preventive, and precise in the coming years."}

def approval_node(state: State) -> Command[Literal["finalize_doc", END]]:
    thread_id = state["thread_id"]
    approve_url = f"http://localhost:8005/approve?thread_id={thread_id}"
    reject_url = f"http://localhost:8005/reject?thread_id={thread_id}"

    email_body = f"""
Document for Approval: {state['topic']}

{state['document']}

✅ Approve: {approve_url}
❌ Reject: {reject_url}
"""
    send_approval_email.invoke({
        "to": "approver@example.com",
        "subject": f"Approval Needed: {state['topic']}",
        "body": email_body
    })

    return interrupt({"status": "waiting for approval"})

def finalize_doc(state: State) -> dict:
    print("✅ Document finalized:", state["document"])
    return {}


conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory= SqliteSaver(conn)
builder = StateGraph(State)

builder.add_node("generate_doc", generate_doc)
builder.add_node("approval_node", approval_node)
builder.add_node("finalize_doc", finalize_doc)

builder.set_entry_point("generate_doc")
builder.add_edge("generate_doc", "approval_node")
builder.add_edge("approval_node", "finalize_doc")
builder.add_edge("finalize_doc", END)

graph = builder.compile(checkpointer=memory)


