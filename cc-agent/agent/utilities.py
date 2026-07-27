import os
import sys
import re
import json
import subprocess
from pathlib import Path


# ---------------------------------------------------------
# PATHS and SCRIPTS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "../results")
TRACES_DIR = os.path.join(BASE_DIR, "../results")
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "system_prompt.txt")
IFA_SCRIPT = os.path.join(BASE_DIR, "tools/generate_ifa_report.py")
GET_CC_SCRIPT = os.path.join(BASE_DIR, "tools/get_current_cc.py")
DELEGATE_CC_PATH = "/sys/module/tcp_proxy/parameters/delegate_cc"
CC_MANAGER_SCRIPT = os.path.join(BASE_DIR, "..", "cc")

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
    

def generate_ifa_report(exp_dir, evaluation):
    dst = os.path.join(exp_dir, f"IFA_Report_{evaluation}.txt")

    subprocess.run(
        [sys.executable, IFA_SCRIPT, dst],
        check=True,
    )

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
        if action is None:
            json.dump({"status": "no_action", "Decision": "1"}, f, indent=4)
            print(f"[Agent] No action taken")
        else:
            json.dump(action.model_dump(), f, indent=4) # print the model dump instead of the object itself
        
        short_path = Path(*Path(path).parts[-4:])
        print(f"[Agent] Action saved → {short_path}")


def escape_braces(text):
    return text.replace("{", "{{").replace("}", "}}")


def check_termination_flag(exp_id):
    flag = os.path.join(RESULTS_DIR, exp_id, "terminated")

    if os.path.exists(flag):
        os.remove(flag)
        return True

    return False

def switch_congestion_control(new_cc):
    current_cc = get_current_cc()
    if current_cc == "unknown":
        return False
    if current_cc == new_cc:
        return True

    # NEW: check availability first, fall back to `cc -a` to load+activate
    if not is_cc_available(new_cc):
        print(f"[Agent] '{new_cc}' is not currently loaded. Loading it via the 'cc' manager...")
        try:
            subprocess.run([CC_MANAGER_SCRIPT, "-a", new_cc], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"[Agent] Failed to load/activate '{new_cc}': {e.stderr.strip() if e.stderr else e}")
            return False
        except Exception as e:
            print(f"[Agent] Failed to load/activate '{new_cc}': {e}")
            return False
    else:
        try:
            with open(DELEGATE_CC_PATH, "w") as f:
                f.write(new_cc)
        except Exception as e:
            print(f"[Agent] Failed to switch congestion control: {e}")
            return False

    # NEW: verify it actually took effect, don't just trust "no exception"
    actual_cc = get_current_cc()
    if actual_cc != new_cc:
        print(f"[Agent] Switch to '{new_cc}' did not take effect (active CC is still '{actual_cc}').")
        return False

    print(f"[Agent] Switched from '{current_cc}' to '{new_cc}'.")
    return True

def is_cc_available(name):
    try:
        out = subprocess.check_output(
            ["sysctl", "-n", "net.ipv4.tcp_available_congestion_control"],
            text=True,
        )
        return name in out.strip().split()
    except Exception as e:
        print(f"[Agent] Could not query available CC schemes: {e}")
        return False