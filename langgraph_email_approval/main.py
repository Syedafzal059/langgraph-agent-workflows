from langgraph_email_approval.graph import graph
import uuid

# 🔐 Generate unique thread ID for this run
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# ✅ Initial state with topic
initial_input = {
    "topic": "AI in Healthcare",
    "thread_id": thread_id
}

print(f"🚀 Starting graph with thread ID: {thread_id}")

# 🔄 Run until graph pauses at interrupt
for event in graph.stream(initial_input, config=config, stream_mode="updates"):
    print("📥 EVENT:", event)

    # Print current state snapshot
    current_state = graph.get_state(config)
    print("📦 STATE:", current_state, flush=True)

    # Detect pause (email approval)
    if "__interrupt__" in event:
        print("⏸️ Waiting for human approval via email...")
        print(f"🔗 Use this in email links: http://<your_ip>:8000/approve?thread_id={thread_id}")
        break
