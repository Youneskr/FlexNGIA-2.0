import sys
import os
import json
import time
import subprocess
import re
from dotenv import load_dotenv

# LangGraph & AI
from langgraph.graph import StateGraph, END

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

# Import Schemas & Tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.tools import compiler, trace_logger
from agent.schemas import AgentState, EvaluatorOutput, ArchitectOutput, CoderOutput

# Load Env
load_dotenv()

# --- LLM SETUP (GROQ) ---
# Llama 3.3 70B is powerful and extremely fast on Groq
# llm = ChatGroq(
#     model="llama-3.3-70b-versatile", 
#     temperature=0.1,
#     api_key=os.getenv("GROQ_API_KEY")
# )

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0 # Low temp for precision
)

# llm = ChatOpenAI(
#     # Recommended models: 
#     # - "google/gemini-2.0-flash-001" (Fast, Smart, Cheap)
#     # - "anthropic/claude-3.5-sonnet" (Best Coding Logic)
#     model="meta-llama/llama-3.3-70b-instruct:free", 
#     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1",
#     temperature=0.1
# )

# llm = ChatOpenAI(
#     # Your local model name from 'ollama list'
#     model="deepseek-r1:1.5b",
#     base_url="http://192.168.1.5:11434/v1",
#     # API key is required by the library but ignored by Ollama
#     api_key="ollama",     
#     temperature=0.1
# )


def get_next_version_name(current_cc_name: str) -> str:
    # Pattern to find _vX at the end
    match = re.search(r'llm_cc_v(\d+)', current_cc_name)
    
    if match:
        # Found existing version, increment it
        version = int(match.group(1)) + 1
        return f"llm_cc_v{version}"
    else:
        # No version found (e.g., "cubic", "reno"), start at v1
        return "llm_cc_v1"


# --- NODE 1: EVALUATOR ---
def evaluator_node(state: AgentState):
    print("--- [Node 1] Evaluator: Performing 7-Step Analysis... ---")

    next_name = get_next_version_name(state["current_cc"])
    print(f"[*] Target Algorithm Name: {next_name}")
    
    structured_llm = llm.with_structured_output(EvaluatorOutput)
    
    prompt = ChatPromptTemplate.from_template(
        """You are a Network Performance Expert.
        
        CONTEXT:
        - Current CC: {current_cc}
        - Metrics: {metrics}
        - Target QoS: Throughput > 50Mbps, Latency < 20ms
        
        TASK:
        Perform a rigorous 7-step analysis of the network state.
        
        1. Identify & Analyze: Current CC behavior, environment, and status.
        2. Extract Metrics: Trends from the provided metrics report.
        3. QoS Check: Compare metrics vs targets.
        4. Detect Mismatches: Why is the current CC failing? Link to specific behaviors (e.g. loss-based vs delay-based).
        5. Identify Weaknesses: What traits are missing? (e.g. "Too aggressive", "Passive recovery").
        6. Suggest Improvements: What logic should the new CC add? (e.g. "Delay-based backoff").
        7. Prediction: How will the new design solve the problem?
        
        Output MUST be structured into these exact 7 fields.
        """
    )
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "current_cc": state["current_cc"], 
        "metrics": json.dumps(state["metrics"])
    })
    
    return {
            "evaluator_data": result,
            "target_cc_name": next_name
        }

# --- NODE 2: ARCHITECT ---
def architect_node(state: AgentState):
    print("--- [Node 2] Architect: Designing Strategy based on Analysis... ---")
    
    structured_llm = llm.with_structured_output(ArchitectOutput)
    
    eval_data = state["evaluator_data"]
    
    analysis_context = f"""
    1. STATUS: {eval_data.step_1}
    2. METRICS: {eval_data.step_2}
    3. QOS CHECK: {eval_data.step_3}
    4. MISMATCHES: {eval_data.step_4}
    5. WEAKNESSES: {eval_data.step_5}
    6. SUGGESTIONS: {eval_data.step_6}
    7. PREDICTION: {eval_data.step_7}
    """
    
    prompt = ChatPromptTemplate.from_template(
        """You are a TCP Algorithm Architect.
        
        EVALUATOR'S 7-STEP DIAGNOSIS:
        {analysis_context}
        
        TASK:
        Design a new TCP Congestion Control algorithm 'llm_cc' specifically to address the findings above.
        
        1. Review the 'SUGGESTIONS' (Step 6) and 'WEAKNESSES' (Step 5).
        2. Define the mathematical LOGIC for:
           - ssthresh (Slow Start Threshold)
           - cong_avoid (Congestion Avoidance)
           - undo_cwnd (Loss Recovery)
           
        Do NOT write C code yet. Focus on the Logic and Math.
        """
    )
    chain = prompt | structured_llm
    
    result = chain.invoke({"analysis_context": analysis_context})
    
    return {"architect_data": result}

# --- NODE 3: CODER (STRICT SKELETON) ---
def coder_node(state: AgentState):
    target_name = state.get("target_cc_name", "llm_cc")
    print(f"--- [Node 3] Coder: Writing {target_name}... ---")
    
    structured_llm = llm.with_structured_output(CoderOutput)
    design_json = state["architect_data"].model_dump_json()
    
    if state["error"]:
        instruction = (
            f"CRITICAL: The previous code failed to compile.\n"
            f"COMPILER LOG:\n{state['compiler_output']}\n\n"
            f"PREVIOUS CODE THAT FAILED:\n```c\n{state['c_code']}\n```\n\n"
            f"TASK: Fix the error in the code above while maintaining the strict skeleton below."
        )
    else:
        instruction = f"Implement the strategy for '{target_name}' using the strict skeleton."

    prompt = ChatPromptTemplate.from_template(
        """
        You are an Expert Linux Kernel Developer.
        Task: Write a Loadable TCP Congestion Control Module.

        INPUTS:
        - DESIGN: {design_json}
        - NAME: {target_name}
        - INSTRUCTION: {instruction}

        ============================================================
        ARCHITECTURAL CONSTRAINTS
        ============================================================
        1. **STATELESS DESIGN**: 
           - Do NOT use private data (icsk_ca_priv).
           - Do NOT use `inet_csk_ca`.
           - Rely only on `struct tcp_sock` fields (snd_cwnd, srtt_us, etc.) and global static variables if absolutely necessary for the algorithm logic.
        
        2. **STRICT KERNEL ABI**:
           - Use `max_t(u32, a, b)` for calculations to avoid type errors.
           - Access RTT via `tp->rtt_min.min`.
           - Always pass `struct sock *sk` to helper functions (like `tcp_is_cwnd_limited(sk)`), NOT `tp`.

        3. **SKELETON COMPLIANCE**:
           - Use the provided skeleton EXACTLY.
           - Do NOT add new headers.
           - Do NOT change the `tcp_congestion_ops` struct.

        ============================================================
        REQUIRED SKELETON
        ============================================================
        ```c
        #include <linux/module.h>
        #include <linux/init.h>
        #include <linux/types.h>
        #include <linux/kernel.h>
        #include <net/tcp.h>

        /* FlexNGIA-LLM Generated Logic */

        static u32 {target_name}_ssthresh(struct sock *sk)
        {{
            const struct tcp_sock *tp = tcp_sk(sk);
            
            /* >>> IMPLEMENTATION HERE <<< */
            /* Implement the Slow Start Threshold logic based on the design. */
            /* Default fallback: */
            return max_t(u32, tp->snd_cwnd >> 1, 2U * tp->mss_cache);
        }}

        static void {target_name}_cong_avoid(struct sock *sk, u32 ack, u32 acked)
        {{
            struct tcp_sock *tp = tcp_sk(sk);
            
            /* >>> IMPLEMENTATION HERE <<< */
            /* Implement the Congestion Avoidance logic based on the design. */
            /* Use: tcp_slow_start(tp, acked) and tcp_cong_avoid_ai(tp, tp->snd_cwnd, acked) */
        }}

        static u32 {target_name}_undo_cwnd(struct sock *sk)
        {{
            const struct tcp_sock *tp = tcp_sk(sk);
            /* >>> IMPLEMENTATION HERE <<< */
            return tp->snd_cwnd;
        }}

        static struct tcp_congestion_ops {target_name} __read_mostly = {{
            .name       = "{target_name}",
            .owner      = THIS_MODULE,
            .ssthresh   = {target_name}_ssthresh,
            .cong_avoid = {target_name}_cong_avoid,
            .undo_cwnd  = {target_name}_undo_cwnd,
        }};

        static int __init {target_name}_register(void)
        {{
            return tcp_register_congestion_control(&{target_name});
        }}

        static void __exit {target_name}_unregister(void)
        {{
            tcp_unregister_congestion_control(&{target_name});
        }}

        module_init({target_name}_register);
        module_exit({target_name}_unregister);

        MODULE_AUTHOR("FlexNGIA Agent");
        MODULE_LICENSE("GPL");
        MODULE_DESCRIPTION("LLM Generated CC");
        ```
        """
    )
    
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "design_json": design_json,
        "target_name": target_name,
        "instruction": instruction,
    })
    
    code = result.c_code

    # Static Guard against forbidden dangerous patterns
    if "kmalloc" in code or "icsk_ca_priv" in code:
        return {
            "c_code": "", 
            "error": True, 
            "compiler_output": "STATIC CHECK: Code violated 'Stateless' constraint (found kmalloc or icsk_ca_priv)."
        }

    return {"c_code": code}

# --- NODE 4: COMPILER ---
def compiler_node(state: AgentState):
    print("--- [Node 4] Compiler: Building Module... ---")
    
    success, message = compiler.compile_and_load(state["c_code"], state["target_cc_name"])
    
    if success:
        print("[Compiler] Success!")
        return {"error": False, "compiler_output": "Success"}
    else:
        print(f"[Compiler] Failed! Error Log: {message[:100]}...")
        return {
            "error": True, 
            "compiler_output": message, 
            "retry_count": state["retry_count"] + 1
        }

# --- NODE 5: LOGGER ---
def logger_node(state: AgentState):
    print("--- [Node 5] Logger: Saving Trace... ---")
    
    ai_response_snapshot = {
        "evaluator": state["evaluator_data"].model_dump() if state["evaluator_data"] else None,
        "architect": state["architect_data"].model_dump() if state["architect_data"] else None,
        "code_snippet": state["c_code"][:100] + "..."
    }

    trace_logger.save_trace(
        session_id=state["session_id"],
        step_num=state["step_count"],
        metrics=state["metrics"],
        current_cc=state["current_cc"],
        ai_response_obj=ai_response_snapshot,
        compilation_success=not state["error"]
    )
    return {}

# --- GRAPH EDGES ---
def should_retry(state: AgentState):
    if state["error"]:
        if state["retry_count"] < 3:
            return "coder"
        return "logger"
    return "logger"

# --- GRAPH BUILD ---
workflow = StateGraph(AgentState)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("compiler", compiler_node)
workflow.add_node("logger", logger_node)

workflow.set_entry_point("evaluator")
workflow.add_edge("evaluator", "architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "compiler")
workflow.add_conditional_edges("compiler", should_retry, {"coder": "coder", "logger": "logger"})
workflow.add_edge("logger", END)

app = workflow.compile()

# --- MAIN LOOP ---
def main():
    print("[Graph] FlexNGIA Groq Agent Initialized (Llama 3.3).")
    
    current_session_id = "0" 
    step_counter = 1
    
    while True:
        print(f"\n=== CYCLE START (Step {step_counter}) ===")
        try:
            metrics_out = subprocess.check_output(['python3', 'agent/tools/get_metrics_summary.py'])
            cc_out = subprocess.check_output(['python3', 'agent/tools/get_current_cc.py'])
            metrics = json.loads(metrics_out)
            current_cc = json.loads(cc_out).get('current_cc', 'unknown')
        except:
            print("[Graph] Waiting for tools...")
            time.sleep(10)
            continue

        if 'error' in metrics:
            print(f"[Graph] Metrics Status: {metrics['error']}")
            time.sleep(10)
            continue
            
        detected_session = metrics.get('file', 'unknown').replace('.csv', '')
        if detected_session != current_session_id:
            current_session_id = detected_session
            step_counter = 1
            
        initial_state = {
            "session_id": current_session_id,
            "step_count": step_counter,
            "metrics": metrics,
            "current_cc": current_cc,
            "retry_count": 0,
            "error": False,
            "evaluator_data": None,
            "architect_data": None,
            "c_code": "",
            "compiler_output": ""
        }
        
        try:
            config = {"metadata": {"session_id": current_session_id, "step": step_counter}}
            app.invoke(initial_state, config=config)
            step_counter += 1
        except Exception as e:
            print(f"!!! GRAPH ERROR: {e}")
            import traceback
            traceback.print_exc()
            
        print("[Graph] Cycle Complete. Sleeping 60s...")
        time.sleep(60)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Error: Must run as root.")
        exit(1)
    main()