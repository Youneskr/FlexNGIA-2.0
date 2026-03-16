import os
import sys
import json
import time
import re
import subprocess
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from schemas import AgentOutput
from tools import compiler

load_dotenv()

# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

# GEMINI
# llm = ChatGoogleGenerativeAI(
#     model="gemini-3-flash-preview",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0
# )

# GROQ
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
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

    # find latest directory in RESULTS_DIR
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

# ---------------------------------------------------------
# LLM EXECUTION
# ---------------------------------------------------------

def run_llm(system_prompt, ifa_report, target_name, previous_code=None, current_code=None, compile_error=None):
    context = ifa_report

    # FIRST ATTEMPT → use previous evaluation code
    if previous_code and not current_code:
        context += f"""
            === PREVIOUS GENERATED CONGESTION CONTROL CODE ===
            ```c
                {escape_braces(previous_code)}
            ```
            You may refine or improve this algorithm if necessary.
        """

    # REPAIR ATTEMPT → use failing code
    if current_code:
        context += f"""
            === CURRENT GENERATED CODE (FAILED TO COMPILE) ===
            ```c
                {escape_braces(current_code)}
            ```
            The code above failed compilation. Fix it.
        """

    if compile_error:
        context += f"""
        === COMPILATION ERROR ===
        {compile_error}
        Fix the kernel code so it compiles successfully.
        """

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

def compile_with_self_repair(system_prompt, report, target_cc, session_dir, evaluation, previous_code, session_id):
    compile_error = None
    last_generated_code = None
    result = None

    for attempt in range(3):
        print(f"[Agent] LLM attempt {attempt+1}")

        if check_termination_flag(session_id):
                break

        result = run_llm(
                    system_prompt,
                    report,
                    target_cc,
                    previous_code if attempt == 0 else None,
                    current_code=last_generated_code,
                    compile_error=compile_error
                )
        code = result.c_code
        last_generated_code = code
        success, message = compiler.compile_and_load(code, target_cc)

        if success:
            print("[Compiler] SUCCESS")
            save_generated_code(session_dir, evaluation, code, session_id)
            return result, True

        else:
            print("[Compiler] ERROR — requesting repair")
            compile_error = message

        if check_termination_flag(session_id):
                break

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

    system_prompt = open(SYSTEM_PROMPT_PATH).read()

    print("\n========== [Agent] Checking for new sessions...")
    while True:
        session_id = detect_new_session()

        if not session_id:
            time.sleep(5)
            continue

        print(f"\n[FlexNGIA] NEW SESSION DETECTED → {session_id}")
        session_dir = os.path.join(TRACES_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)

        evaluation = 1

        print("[FlexNGIA] Waiting 60 seconds before first evaluation")
        terminated = False
        for _ in range(60):
            if check_termination_flag(session_id):
                print(f"[FlexNGIA] Session {session_id} terminated")
                terminated = True
                break
            time.sleep(1)

        if terminated:
            continue

        while True:
            print(f"\n========== SESSION {session_id} | EVALUATION {evaluation} ==========")
            current_cc = get_current_cc()
            print(f"[Agent] Current CC: {current_cc}")

            target_cc = get_next_version_name(current_cc, session_id)
            if check_termination_flag(session_id):
                print(f"[FlexNGIA] Session {session_id} terminated")
                break
            print(f"[Agent] Target CC: {target_cc}")

            generate_ifa_report()
            ifa_path = move_ifa_report(session_dir, evaluation)
            print("[Agent] Receiving IFA report")
            report = open(ifa_path).read()

            previous_code = get_previous_code(session_dir, evaluation, session_id)

            if check_termination_flag(session_id):
                print(f"[FlexNGIA] Session {session_id} terminated")
                break

            print("[Agent] Running LLM reasoning")
            result, compiled = compile_with_self_repair(
                system_prompt, 
                report, 
                target_cc, 
                session_dir, 
                evaluation, 
                previous_code, 
                session_id)

            if result is None:
                break

            if check_termination_flag(session_id):
                print(f"[FlexNGIA] Session {session_id} terminated")
                break

            save_action(session_dir, evaluation, result)


            if not compiled:
                print("[Agent] Compilation failed after retries")

            evaluation += 1

            print("[Agent] Sleeping 60 seconds")
            terminated = False
            for _ in range(60):
                if check_termination_flag(session_id):
                    print(f"[FlexNGIA] Session {session_id} terminated")
                    terminated = True
                    break
                time.sleep(1)
            if terminated:
                break

# ---------------------------------------------------------
if __name__ == "__main__":
    main()