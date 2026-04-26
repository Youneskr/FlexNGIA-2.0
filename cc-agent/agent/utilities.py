import os
import sys
import re
import json
import subprocess


# ---------------------------------------------------------
# PATHS and SCRIPTS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "../results")
TRACES_DIR = os.path.join(BASE_DIR, "../results")
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
IFA_SCRIPT = os.path.join(BASE_DIR, "tools/generate_ifa_report.py")
GET_CC_SCRIPT = os.path.join(BASE_DIR, "tools/get_current_cc.py")


# ---------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------

def get_next_version_name(current_cc_name: str, exp_id: str) -> str:
    match = re.search(rf"llm_cc_{exp_id}_(\d+)", current_cc_name)

    if match:
        version = int(match.group(1)) + 1
        return f"llm_cc_{exp_id}_{version}"
    else:
        return f"llm_cc_{exp_id}_1"


def detect_new_experiment():
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

#Generate IFA report by running the IFA script defined above
def generate_ifa_report():
    subprocess.run([sys.executable, IFA_SCRIPT])


def move_ifa_report(exp_dir, evaluation):
    src = os.path.join(BASE_DIR, "IFA_Report_Filled.tmp.txt")
    dst = os.path.join(exp_dir, f"IFA_Report_{evaluation}.txt")
    os.rename(src, dst)
    return dst


def get_previous_code(exp_dir, evaluation, exp_id):
    if evaluation <= 1:
        return None

    prev_file = os.path.join(exp_dir, f"llm_cc_{exp_id}_{evaluation-1}.c")

    if os.path.exists(prev_file):
        with open(prev_file) as f:
            return f.read()

    return None


def save_generated_code(exp_dir, evaluation, code, exp_id):
    code_path = os.path.join(exp_dir, f"llm_cc_{exp_id}_{evaluation}.c")
    with open(code_path, "w") as f:
        f.write(code)
    return code_path


def save_action(exp_dir, evaluation, action):
    path = os.path.join(exp_dir, f"action_{evaluation}.json")
    with open(path, "w") as f:
        json.dump(action.model_dump(), f, indent=4)
    print(f"[Agent] Action saved → {path}")


def escape_braces(text):
    return text.replace("{", "{{").replace("}", "}}")


def check_termination_flag(exp_id):
    flag = os.path.join(RESULTS_DIR, exp_id, "terminated")

    if os.path.exists(flag):
        os.remove(flag)
        return True

    return False