import os
import json
import time

# agent/tools/ -> agent/traces/
BASE_TRACE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'traces')

def save_trace(session_id, step_num, metrics, current_cc, ai_response_obj, compilation_success):
    """
    Saves the full context of an agent action to a JSON file.
    Path: agent/traces/<session_id>/action-<step_num>.json
    """
    # 1. Ensure directory exists
    session_dir = os.path.join(BASE_TRACE_DIR, str(session_id))
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
        print(f"[Logger] Created new trace directory: {session_dir}")

    # 2. Prepare Data
    # Convert Pydantic object to dict if needed
    if hasattr(ai_response_obj, 'model_dump'):
        decision_data = ai_response_obj.model_dump()
    else:
        decision_data = ai_response_obj

    trace_data = {
        "timestamp": time.time(),
        "step": step_num,
        "session_id": session_id,
        "input_context": {
            "active_cc": current_cc,
            "metrics": metrics
        },
        "ai_output": decision_data,
        "outcome": {
            "compilation_success": compilation_success
        }
    }

    # 3. Write to File
    filename = f"action-{step_num}.json"
    filepath = os.path.join(session_dir, filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(trace_data, f, indent=4)
        print(f"[Logger] Trace saved to: {filepath}")
        return True
    except Exception as e:
        print(f"[Logger] Error saving trace: {e}")
        return False