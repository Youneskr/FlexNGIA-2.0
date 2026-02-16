from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

# --- NODE OUTPUT SCHEMAS ---

class EvaluatorOutput(BaseModel):
    """Output for Node 1: Deep Analysis (Steps 1-7)"""
    
    # Step 1
    step_1: str = Field(description="1. Analyze current CC, environment, and QoS/QoE status.")
    # Step 2
    step_2: str = Field(description="2. Key metrics and trends extracted from the report.")
    # Step 3
    step_3: str = Field(description="3. QoS Profile Check: Are targets (T > 50Mbps, L < 20ms) met?")
    # Step 4
    step_4: str = Field(description="4. Detect mismatches and link them to Current CC behavior.")
    # Step 5
    step_5: str = Field(description="5. Identify missing traits (e.g., lack of delay sensitivity).")
    # Step 6
    step_6: str = Field(description="6. Suggest specific behavioral improvements.")
    # Step 7
    step_7: str = Field(description="7. Predict how a new algorithm will improve performance.")
    
    # Summary for quick reference
    recommendation: str = Field(description="A one-sentence summary of the required change.")

class ArchitectOutput(BaseModel):
    """Output for Node 2: Strategy Design"""
    strategy_name: str = Field(description="Name of the new strategy (e.g., 'DelayBoundedReno').")
    ssthresh_logic: str = Field(description="Mathematical logic for Slow Start Threshold.")
    cong_avoid_logic: str = Field(description="Mathematical logic for Congestion Avoidance.")
    undo_cwnd_logic: str = Field(description="Mathematical logic for Undo/Recovery.")
    justification: str = Field(description="Why this design will fix the identified weaknesses.")

class CoderOutput(BaseModel):
    """Output for Node 3: Implementation"""
    c_code: str = Field(description="The complete, valid C code for the Linux Kernel module.")

# --- SHARED GRAPH STATE ---

class AgentState(TypedDict):
    """The memory passed between nodes"""
    session_id: str
    step_count: int
    metrics: dict
    current_cc: str
    target_cc_name: str
    
    # 7-step analysis
    evaluator_data: Optional[EvaluatorOutput]
    architect_data: Optional[ArchitectOutput]
    
    # Execution
    c_code: str
    compiler_output: str
    error: bool
    retry_count: int