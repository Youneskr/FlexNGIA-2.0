from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    """Output for Node 1: Deep Analysis (Steps 1-7)"""
    step_1: str = Field(description="1. Analyze current CC, environment, and QoS/QoE status.")
    step_2: str = Field(description="2. Key metrics and trends extracted from the report.")
    step_3: str = Field(description="3. QoS Profile Check: Are targets (T > 50Mbps, L < 20ms) met?")
    step_4: str = Field(description="4. Detect mismatches and link them to Current CC behavior.")
    step_5: str = Field(description="5. Identify missing traits (e.g., lack of delay sensitivity).")
    step_6: str = Field(description="6. Suggest specific behavioral improvements.")
    step_7: str = Field(description="7. Predict how a new algorithm will improve performance.")
    step_8: str = Field(description="Why this design will fix the identified weaknesses.")
    c_code: str = Field(description="The complete, valid C code for the Linux Kernel module.")