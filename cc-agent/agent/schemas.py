from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    """Output of the LLM agent, including the generated C code and the 8 reasoning steps."""
    step_1: str = Field(description="Step 1: Identify and analyze the current congestion control algorithm, environment, and QoS/QoE status.")
    step_2: str = Field(description="Step 2: Extract key metrics and trends from the IFA report.")
    step_3: str = Field(description="Step 3: Recall the application’s target QoS profile and check if they are met.")
    step_4: str = Field(description="Step 4: Detect (if exist) performance mismatches and link them to Current algorithm behavior.")
    step_5: str = Field(description="Step 5: Identify missing or weak control traits (if exist).")
    step_6: str = Field(description="Step 6: Suggest parameter adjustments or behavioral improvements.")
    step_7: str = Field(description="Step 7: Predict how a new algorithm will improve performance.")
    step_8: str = Field(description="Step 8: Choose the best action and briefly justify it.")
    c_code: str = Field(description="The complete, valid C code for the Linux Kernel module.")