import os
import sys
import re
import json
import subprocess


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "../results")
TRACES_DIR = os.path.join(BASE_DIR, "traces")
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
IFA_SCRIPT = os.path.join(BASE_DIR, "tools/generate_ifa_report.py")
GET_CC_SCRIPT = os.path.join(BASE_DIR, "tools/get_current_cc.py")


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def get_next_version_name(current_cc_name: str, session_id: str) -> str:
    match = re.search(rf"llm_cc_{session_id}_(\d+)", current_cc_name)

    if match:
        version = int(match.group(1)) + 1
        return f"llm_cc_{session_id}_{version}"
    else:
        return f"llm_cc_{session_id}_1"


def detect_new_session():
    clock_file = "CLOCK_START"

    if not os.path.exists(clock_file):
        return None

    dirs = [
        d for d in os.listdir(RESULTS_DIR)
        if os.path.isdir(os.path.join(RESULTS_DIR, d))
    ]

    if not dirs:
        print("[Agent] No directories found in RESULTS_DIR")
        return None

    latest = max(dirs, key=lambda x: int(x))

    return latest


def get_current_cc():
    try:
        out = subprocess.check_output([sys.executable, GET_CC_SCRIPT])
        data = json.loads(out)

        if data["status"] == "success":
            return data["current_cc"]

    except Exception:
        pass

    return "unknown"


def generate_ifa_report():
    subprocess.run([sys.executable, IFA_SCRIPT])


def move_ifa_report(session_dir, evaluation):
    src = os.path.join(BASE_DIR, "traces/IFA_Report_Filled.txt")
    dst = os.path.join(session_dir, f"IFA_Report_{evaluation}.txt")
    os.rename(src, dst)
    return dst


def get_previous_code(session_dir, evaluation, session_id):
    if evaluation <= 1:
        return None

    prev_file = os.path.join(session_dir, f"llm_cc_{session_id}_{evaluation-1}.c")

    if os.path.exists(prev_file):
        with open(prev_file) as f:
            return f.read()

    return None


def save_generated_code(session_dir, evaluation, code, session_id):
    code_path = os.path.join(session_dir, f"llm_cc_{session_id}_{evaluation}.c")
    with open(code_path, "w") as f:
        f.write(code)
    return code_path


def save_action(session_dir, evaluation, action):
    path = os.path.join(session_dir, f"action_{evaluation}.json")
    with open(path, "w") as f:
        json.dump(action.model_dump(), f, indent=4)
    print(f"[Agent] Action saved → {path}")


def escape_braces(text):
    return text.replace("{", "{{").replace("}", "}}")


def check_termination_flag(session_id):
    flag = os.path.join(RESULTS_DIR, session_id, "terminated")

    if os.path.exists(flag):
        os.remove(flag)
        return True

    return False