import os
import sys
import json
import time
import re
import subprocess
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from schemas import AgentOutput
from tools import compiler

load_dotenv()

# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

structured_llm = llm.with_structured_output(AgentOutput)

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

def get_next_version_name(current_cc_name: str) -> str:
    match = re.search(r'llm_cc_v(\d+)', current_cc_name)

    if match:
        version = int(match.group(1)) + 1
        return f"llm_cc_v{version}"
    else:
        return "llm_cc_v1"


def detect_new_session(seen_sessions):
    files = sorted(os.listdir(RESULTS_DIR))

    for f in files:
        if not f.endswith(".csv"):
            continue

        session_id = f.replace(".csv", "")

        if session_id not in seen_sessions:
            seen_sessions.add(session_id)
            return session_id

    return None


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


def move_ifa_report(session_dir, cycle):
    src = os.path.join(BASE_DIR, "traces/IFA_Report_Filled.txt")
    dst = os.path.join(session_dir, f"IFA_Report_{cycle}.txt")
    os.rename(src, dst)
    return dst


def get_previous_code(session_dir, cycle):
    if cycle <= 1:
        return None

    prev_file = os.path.join(session_dir, f"cc_cycle_{cycle-1}.c")

    if os.path.exists(prev_file):
        with open(prev_file) as f:
            return f.read()

    return None


def save_generated_code(session_dir, cycle, code):
    code_path = os.path.join(session_dir, f"cc_cycle_{cycle}.c")
    with open(code_path, "w") as f:
        f.write(code)
    return code_path


def save_action(session_dir, cycle, action):
    path = os.path.join(session_dir, f"action_{cycle}.json")
    with open(path, "w") as f:
        json.dump(action.model_dump(), f, indent=4)
    print(f"[Agent] Action saved → {path}")

def escape_braces(text):
    return text.replace("{", "{{").replace("}", "}}")

# ---------------------------------------------------------
# LLM EXECUTION
# ---------------------------------------------------------

def run_llm(system_prompt, ifa_report, target_name, previous_code=None, compile_error=None):
    context = ifa_report

    if previous_code:
        context += f"""
            === PREVIOUS GENERATED CONGESTION CONTROL CODE ===
            ```c
                {previous_code}
            ```
            You may refine or improve this algorithm if necessary.
        """

    if compile_error:
        context += f"""
        === COMPILATION ERROR ===
        {compile_error}
        Fix the kernel code so it compiles successfully.
        """
    
    context = escape_braces(context)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", context)
    ])

    chain = prompt | structured_llm

    result = chain.invoke({
        "target_name": target_name,
        # "ifa_report": ifa_report
    })

    return result

# ---------------------------------------------------------
# COMPILE WITH SELF-REPAIR
# ---------------------------------------------------------

def compile_with_self_repair(system_prompt, report, target_cc, session_dir, cycle, previous_code):
    compile_error = None

    for attempt in range(3):
        print(f"[Agent] LLM attempt {attempt+1}")

        result = run_llm(system_prompt, report, target_cc, previous_code, compile_error)
        code = result.c_code
        success, message = compiler.compile_and_load(code, target_cc)

        if success:
            print("[Compiler] SUCCESS")
            save_generated_code(session_dir, cycle, code)
            return result, True

        else:
            print("[Compiler] ERROR — requesting repair")
            compile_error = message

    return result, False

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

def main():
    if os.geteuid() != 0:
        print("Error: Must run as root.")
        return

    print("[FlexNGIA] Agent started")

    os.makedirs(TRACES_DIR, exist_ok=True)

    # Ignore pre-existing sessions
    seen_sessions = {
        f.replace(".csv", "")
        for f in os.listdir(RESULTS_DIR)
        if f.endswith(".csv")
    }

    system_prompt = open(SYSTEM_PROMPT_PATH).read()

    while True:
        session_id = detect_new_session(seen_sessions)

        if not session_id:
            time.sleep(5)
            continue

        print(f"\n[FlexNGIA] NEW SESSION DETECTED → {session_id}")
        session_dir = os.path.join(TRACES_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)

        cycle = 1

        print("[FlexNGIA] Waiting 60 seconds before first cycle")
        time.sleep(60)

        while True:
            print(f"\n========== SESSION {session_id} | CYCLE {cycle} ==========")

            current_cc = get_current_cc()
            print(f"[Agent] Current CC: {current_cc}")

            target_cc = get_next_version_name(current_cc)
            print(f"[Agent] Target CC: {target_cc}")

            print("[Agent] Generating IFA report")
            generate_ifa_report()
            ifa_path = move_ifa_report(session_dir, cycle)
            report = open(ifa_path).read()

            previous_code = get_previous_code(session_dir, cycle)

            print("[Agent] Running LLM reasoning")
            result, compiled = compile_with_self_repair(
                system_prompt,
                report,
                target_cc,
                session_dir,
                cycle,
                previous_code
            )

            save_action(session_dir, cycle, result)

            if not compiled:
                print("[Agent] Compilation failed after retries")

            cycle += 1

            print("[Agent] Sleeping 60 seconds")
            time.sleep(60)


# ---------------------------------------------------------
if __name__ == "__main__":
    main()