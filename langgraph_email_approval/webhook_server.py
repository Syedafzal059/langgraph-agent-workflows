from flask import Flask, request, jsonify
import asyncio
from langgraph_email_approval.graph import graph
from langgraph.types import Command


app = Flask(__name__)

@app.route("/approve")
def approve():
    thread_id = request.args.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}

    #🛡️ Verify the thread is waiting at interrupt before resuming
    try:
        state = graph.get_state(config)
        print(f"state server =  {state} ")
        if state.next != ("approval_node",):
            return jsonify({"error": "Not waiting for approval"}), 400
    except Exception as e:
        return jsonify({"error": f"Could not fetch state: {str(e)}"}), 400

    # async def resume():
    #     await graph.ainvoke(Command(resume={"action": "approve"}), config=config)

    #asyncio.run(resume())
    graph.invoke(Command(resume={"action": "approve"}), config=config)

    return jsonify({"status": "✅ Approved and resumed."})

@app.route("/reject")
def reject():
    thread_id = request.args.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}

    try:
        state = graph.get_state(config)
        print(f"state on server = {state} ", flush =True)
        if state.get("next") != ("approval_node",):
            return jsonify({"error": "Not waiting for rejection"}), 400
    except Exception as e:
        return jsonify({"error": f"Could not fetch state: {str(e)}"}), 400

    # async def resume():
    #     await graph.ainvoke(Command(resume={"action": "reject"}), config=config)

    # asyncio.run(resume())
    graph.invoke(Command(resume={"action": "reject"}), config=config)

    return jsonify({"status": "❌ Rejected and halted."})

if __name__ == "__main__":
    app.run(port=8005, debug=True)
