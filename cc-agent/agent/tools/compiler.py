import os
import subprocess
import sys

# Define workspace: agent/workspace/
WORKSPACE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'workspace')
DELEGATE_CC_PATH = "/sys/module/tcp_proxy/parameters/delegate_cc"

def compile_and_load(c_code_content, cc_name):
    """
    Compiles the C code with a dynamic name (e.g. llm_cc_v1).
    """
    if not c_code_content:
        return False, "Error: No C code provided."

    # 1. Prepare Workspace
    try:
        if not os.path.exists(WORKSPACE_DIR):
            os.makedirs(WORKSPACE_DIR)

        # [FIX 1] Dynamic Makefile Target
        makefile_content = f"""
obj-m += {cc_name}.o

all:
\tmake -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) modules

clean:
\tmake -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) clean
"""
        
        with open(os.path.join(WORKSPACE_DIR, 'Makefile'), 'w') as f:
            f.write(makefile_content.strip())

        # [FIX 2] Dynamic C Filename (MUST match cc_name)
        c_file_path = os.path.join(WORKSPACE_DIR, f'{cc_name}.c') 
        with open(c_file_path, 'w') as f:
            f.write(c_code_content)
            
    except Exception as e:
        return False, f"File Write Error: {str(e)}"

    # 2. Compile
    try:
        # We clean first to remove old .o files
        subprocess.run(['make', 'clean'], cwd=WORKSPACE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        result = subprocess.run(
            ['make'], 
            cwd=WORKSPACE_DIR, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            return False, f"COMPILATION ERROR:\n{result.stderr}"
            
    except Exception as e:
        return False, f"Make Process Failed: {str(e)}"

    # 3. Load New Module
    try:
        # [FIX 3] Look for the correctly named .ko file
        ko_file = os.path.join(WORKSPACE_DIR, f'{cc_name}.ko')
        
        if not os.path.exists(ko_file):
            return False, f"Error: {cc_name}.ko not found. Did the makefile build the right target?"

        # Remove if it exists (reload)
        lsmod_out = subprocess.run(['lsmod'], capture_output=True, text=True).stdout
        if cc_name in lsmod_out:
            subprocess.run(['rmmod', cc_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = subprocess.run(
            ['insmod', ko_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, f"INSMOD ERROR:\n{result.stderr}"
        
        # 4. Activate
        if os.path.exists(DELEGATE_CC_PATH):
            with open(DELEGATE_CC_PATH, 'w') as f:
                f.write(cc_name)

            try:
                subprocess.run(
                    'echo "" >> ./clock.log && sudo ./clock.sh get >> ./clock.log',
                    shell=True,
                    check=False
                )
            except Exception as e:
                print(f"[Clock] Logging failed: {e}")

            return True, f"Success: Module {cc_name} loaded and activated."

        else:
            return False, f"Activation Error: {DELEGATE_CC_PATH} not found."        
    except Exception as e:
        return False, f"Loading/Activation Error: {str(e)}"