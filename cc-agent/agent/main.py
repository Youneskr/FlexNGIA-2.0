import os
import time

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from schemas import AgentOutput
from tools import compiler
from utilities import (
    TRACES_DIR,
    SYSTEM_PROMPT_PATH,
    detect_new_session,
    get_current_cc,
    get_next_version_name,
    generate_ifa_report,
    move_ifa_report,
    get_previous_code,
    save_generated_code,
    save_action,
    escape_braces,
    check_termination_flag,
)

load_dotenv()

# ---------------------------------------------------------
# LLM — Uncomment the provider you want to use and pick the model you want to use.
#        Only one `llm = ...` block should be active at a time.
# ---------------------------------------------------------

# GROQ
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)

# GEMINI
# llm = ChatGoogleGenerativeAI(
#     model="",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0,
# )

# OPENAI
# llm = ChatOpenAI(
#     model="",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     temperature=0,
# )

# OPENROUTER (supports any model from openrouter.ai/models)
# llm = ChatOpenAI(
#     model="",
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     base_url="https://openrouter.ai/api/v1",
#     temperature=0,
# )

structured_llm = llm.with_structured_output(AgentOutput)


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
                session_id
            )

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