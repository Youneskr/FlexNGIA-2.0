import os
import time
import random
from pathlib import Path

from dotenv import load_dotenv
ENV_PATH = Path(__file__).resolve().parent / "config.env"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from schemas import AgentOutput
from tools import compiler
from utilities import (
    TRACES_DIR,
    SYSTEM_PROMPT_PATH,
    detect_new_experiment,
    get_current_cc,
    get_next_version_name,
    generate_ifa_report,
    get_previous_code,
    save_generated_code,
    save_action,
    escape_braces,
    check_termination_flag,
    switch_congestion_control,
)

load_dotenv(ENV_PATH)
EvaluationInterval=int(os.getenv("EVALUATION_INTERVAL"))
LLM_ATTEMPTS=int(os.getenv("LLM_ATTEMPTS"))
LLM_Activated=int(os.getenv("LLM_ACTIVATED"))
Available_cc_schemes = os.getenv("AVAILABLE_CC_SCHEMES", "").split(",")
#----------------------------------------------------------
# Decision constants
KEEP_CURRENT_CC = "1"
SWITCH_EXISTING_CC = "2"
GENERATE_NEW_CC = "3"


# ---------------------------------------------------------
# LLM — Uncomment the provider you want to use and pick the model you want to use.
#        Only one `llm = ...` block should be active at a time.
# ---------------------------------------------------------

def load_llm():
    provider   = os.getenv("LLM_PROVIDER", "GROQ").upper()
    model      = os.getenv("LLM_MODEL")
    temperature = float(os.getenv("LLM_TEMPERATURE", 0))

    if provider == "GROQ":
        return ChatGroq(
            model=model,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=temperature,
        )
    elif provider == "GEMINI":
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=temperature,
        )
    elif provider == "OPENAI":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temperature,
        )
    elif provider == "OPENROUTER":
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
        )
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: '{provider}'. Choose from: GROQ, GEMINI, OPENAI, OPENROUTER")


# load the LLM  
if LLM_Activated == 1:
    print("[Agent] LLM is activated... Loading LLM...")
    llm = load_llm()
    # this instruction tells the LLM to return output in a structured format that matches the AgentOutput schema defined in schemas.py
    structured_llm = llm.with_structured_output(AgentOutput)
elif LLM_Activated == 0:
    print("[Agent] LLM is deactivated...")
    llm = None
elif LLM_Activated == 2:
    print("[Agent] LLM is deactivated... Randomly switching to a new CC scheme...")
    llm = None  


# ---------------------------------------------------------
# LLM EXECUTION
# ---------------------------------------------------------
# This function runs the LLM with the appropriate context and 
# handles both the initial code generation and subsequent repair 
# attempts if compilation fails.

def run_llm(system_prompt, ifa_report, target_name, previous_code=None, current_code=None, compile_error=None):
    context = ifa_report

    # FIRST ATTEMPT → use previous evaluation code
    # If this is the first attempt (i.e., no current_code), we provide the previous code to the LLM for reference. 
    # The LLM can choose to refine or improve this code based on the new IFA report.
    # Either we pass the code generated in the last evaluation or the code generated in the current evaluation (if the last one failed to compile). 
    if previous_code and not current_code:
        # Apprend the previous code to the context with formatting
        context += f"""
            === PREVIOUS GENERATED CONGESTION CONTROL CODE ===
            ```c
                {escape_braces(previous_code)}
            ```
            You may refine or improve this algorithm if necessary.
        """

    # REPAIR ATTEMPT → use failing code
    # If the current generated code failed to compile, we provide that code to the LLM along with the compilation error.
    if current_code:
        context += f"""
            === CURRENT GENERATED CODE (FAILED TO COMPILE) ===
            ```c
                {escape_braces(current_code)}
            ```
            The code above failed compilation. Fix it.
        """
    # If there was a compilation error, we include that in the context to help the LLM understand what went wrong and how to fix it.
    if compile_error:
        context += f"""
        === COMPILATION ERROR ===
        {escape_braces(compile_error)}
        Fix the kernel code so it compiles successfully.
        """
    # Finally, we construct the prompt for the LLM, which includes the system prompt (instructions) and the user context (IFA report, previous code, current code, and compile error if applicable).
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", context)
    ])
    # We then create a chain that connects the prompt to the structured LLM output. 
    # When we invoke this chain, it will send the prompt to the LLM and expect a response that can be parsed into the AgentOutput schema.
    chain = prompt | structured_llm

    # We invoke the chain with the target congestion control algorithm name as input. 
    # The LLM will generate code for this target algorithm based on the provided context.
    try:
        result = chain.invoke({
            "target_name": target_name, # name of the file with the new CC algorithm (e.g., "cc_v2")
    })
    except Exception as e:
      print(f"[LLM] Error: {e}")
      return None

    return result


# ---------------------------------------------------------
# GENERATE THE CODE AND COMPILE WITH SELF-REPAIR (3 ATTEMPTS)
# ---------------------------------------------------------
# This function attempts to compile the code generated by the LLM. 
# If compilation fails, it captures the error and provides it back to the LLM for repair.

def compile_with_self_repair(system_prompt, report, target_cc, exp_dir, evaluation, previous_code, exp_id):
    compile_error = None
    last_generated_code = None
    result = None
    # We allow up to LLM_ATTEMPTS attempts for the LLM to generate code that compiles successfully.
    for attempt in range(1, LLM_ATTEMPTS+1):
        print(f"[Agent] LLM attempt {attempt}")

        if check_termination_flag(exp_id):
            break

        result = run_llm(
            system_prompt,
            report,
            target_cc,
            previous_code if attempt == 0 else None,
            current_code=last_generated_code,
            compile_error=compile_error
        )
        if result is None or not hasattr(result, "Decision") or not result.Decision:
            print("[Agent] LLM failed... No results and decisions returned. ")
            continue # skip an iteration from the loop 
        else: 
            Decision= result.Decision
            if Decision == KEEP_CURRENT_CC:
                print("[Agent] LLM decided to keep the current CC scheme")
                return result, True
            elif Decision == SWITCH_EXISTING_CC:
                if not hasattr(result, "switchCC") or not result.switchCC:
                    print("[Agent] LLM decided to switch to an existing CC scheme- but No field `switchCC` returned by the LLM")
                    continue # skip an iteration from the loop
                # We extract the name of the existing congestion control scheme to switch to from the LLM's response. This is expected to be one of the predefined schemes like 'cubic', 'bbr', 'reno', or 'vegas'.
                switchCC = result.switchCC
                print(f"[Agent] LLM decided to switch to existing CC scheme: {switchCC}")
                return result, True
            elif Decision == GENERATE_NEW_CC:
                print("[Agent] LLM decided to generate a new CC scheme")
                if not hasattr(result, "c_code") or not result.c_code: # check if the LLM returned any code at all. If not, we assume the decision was to keep the current CC algorithm and skip to the next evaluation.
                    print("[Agent] No field `c_code` returned by the LLM")
                    continue #    
                # We extract the generated code from the LLM's response and attempt to compile it.
                code = result.c_code # we expect the LLM to return a field named `c_code`, which contains the generated CC algorithm code.
                last_generated_code = code # we keep track of the last generated code so that if compilation fails, we can provide it to the LLM for repair in the next attempt.
                success, message = compiler.compile_and_load(code, target_cc) # Compile the generated code. The `compile_and_load` function returns a boolean indicating success or failure, and a message that contains either the success confirmation or the compilation error.

                if success:
                    print(f"[Compiler] Compilation succeeded: Target CC: {target_cc}")
                    save_generated_code(exp_dir, evaluation, code, exp_id)
                    return result, True
                else:
                    print("[Compiler] Compilation error ")
                    compile_error = message

        if check_termination_flag(exp_id):
            break
    if attempt==LLM_ATTEMPTS:
        Decision = KEEP_CURRENT_CC
        print(f"[Agent] No valid code generated after {LLM_ATTEMPTS} attempts. Same CC Scheme will be kept.")
        return result, True
    
    print(f"[Agent] function compile_with_self_repair(): {attempt}/{LLM_ATTEMPTS} \n should never reach this line")


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
    # replace {Available_cc_schemes} in system_prompt with the actual list of available congestion control schemes from the environment variable. This allows the LLM to know which existing schemes it can switch to if it decides to do so.
    system_prompt = system_prompt.replace("{Available_cc_schemes}", ", ".join(Available_cc_schemes))    

    print("\n========== [Agent] Checking for new experiments...")
    while True:
        exp_id = detect_new_experiment()

        if not exp_id:
            time.sleep(5)
            continue

        print(f"\n[FlexNGIA] NEW EXPERIMENT DETECTED - Experiment ID: {exp_id}")
        exp_dir = os.path.join(TRACES_DIR, exp_id)
        os.makedirs(exp_dir, exist_ok=True)

        evaluation = 1

        print(f"[FlexNGIA] Waiting {EvaluationInterval} seconds before evaluation {evaluation}...")
        terminated = False
        for _ in range(EvaluationInterval):
            if check_termination_flag(exp_id):
                print(f"[FlexNGIA] EXPERIMENT {exp_id} terminated")
                terminated = True
                break
            time.sleep(1)

        if terminated:
            continue
        
        # Now we enter the main evaluation loop for this experiment. 
        # The agent will continuously monitor the experiment, generate IFA reports, 
        # run the LLM to get new congestion control code, attempt to compile it, 
        # and if it fails, provide feedback to the LLM for repairs. 
        # This loop continues until a termination flag is detected for the experiment   .
        while True:
            print(f"\n========== EXPERIMENT {exp_id} | EVALUATION {evaluation} ==========")
            #Check the current CC algorithm being used in the experiment. This is important for the LLM to know so it can generate code that is an improvement over the current version.
            current_cc = get_current_cc()
            print(f"[Agent] Current CC: {current_cc}")

            # Determine the target CC algorithm name for this evaluation. This is typically a new version name (e.g., "cc_v2", "cc_v3", etc.) that the LLM will generate code for.
            target_cc = get_next_version_name(current_cc, exp_id)
            if check_termination_flag(exp_id):
                print(f"[FlexNGIA] Experiment {exp_id} terminated")
                break
            # print(f"[Agent] Target CC: {target_cc}")

            # Generate the IFA report for the current experiment. The IFA report contains detailed information about the experiment's network conditions and performance, which serves as critical context for the LLM to generate effective congestion control code.
            ifa_path = generate_ifa_report(exp_dir, evaluation)
            #ifa_path = move_ifa_report(exp_dir, evaluation)
            if not os.path.exists(ifa_path):  
                print(f"[Agent] IFA report not found at {ifa_path}. Skipping evaluation {evaluation}.")
            else:
                print("[Agent] Receiving IFA report")
                report = open(ifa_path).read()

            previous_code = get_previous_code(exp_dir, evaluation, exp_id)

            if check_termination_flag(exp_id):
                print(f"[FlexNGIA] Experiment {exp_id} terminated")
                break
            
            result = None  
            
            if LLM_Activated == 1: 
                print("[Agent] Running LLM reasoning")
                result, compiled = compile_with_self_repair(
                    system_prompt,
                    report,
                    target_cc,
                    exp_dir,
                    evaluation,
                    previous_code,
                    exp_id
                )
            elif LLM_Activated == 0:
                print("[Agent] LLM is deactivated. Keeping the current CC scheme.")
            elif LLM_Activated == 2:
                # we choose randomly a CC scheme from the Available_cc_schemes available ones but different from the current
                new_cc = random.choice([cc for cc in Available_cc_schemes if cc != current_cc])
                print(f"[Agent] Randomly switching to a new CC scheme: {new_cc}")
                switch_congestion_control(new_cc)  
                result = AgentOutput(
                    step_1="LLM disabled (LLM_ACTIVATED=2): current CC and environment not analyzed by an LLM.",
                    step_2="N/A - no IFA report analysis performed in random-switch mode.",
                    step_3="N/A - no QoS/QoE profile evaluation performed in random-switch mode.",
                    step_4="N/A - no performance mismatch detection performed in random-switch mode.",
                    step_5="N/A - no control trait analysis performed in random-switch mode.",
                    step_6="N/A - no parameter/behavioral suggestions in random-switch mode.",
                    step_7="N/A - no improvement prediction in random-switch mode.",
                    step_8=(f"Randomly selected '{new_cc}' from the available schemes and "),
                    Decision=SWITCH_EXISTING_CC,
                    switchCC=new_cc,
                    c_code="",
                )  


            if check_termination_flag(exp_id):
                print(f"[FlexNGIA] Experiment {exp_id} terminated")
                break
          
            save_action(exp_dir, evaluation, result)

            #if not compiled:
                #print("[Agent] Compilation failed after retries")

            evaluation += 1

            print(f"[Agent] Sleeping {EvaluationInterval} seconds")
            terminated = False
            for _ in range(EvaluationInterval):
                if check_termination_flag(exp_id):
                    print(f"[FlexNGIA] Experiment {exp_id} terminated")
                    terminated = True
                    break
                time.sleep(1)
            if terminated:
                break


# ---------------------------------------------------------
if __name__ == "__main__":
    main()
