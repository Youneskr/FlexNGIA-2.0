import json
import sys
import os

# Path to your custom module parameter
DELEGATE_CC_PATH = "/sys/module/tcp_proxy/parameters/delegate_cc"

def main():
    try:
        # Check if the file exists (Is the module loaded?)
        if not os.path.exists(DELEGATE_CC_PATH):
            print(json.dumps({
                "status": "error",
                "message": f"Parameter file not found: {DELEGATE_CC_PATH}",
                "details": "Is the tcp_proxy module loaded?"
            }))
            return

        # Read the current CC name
        with open(DELEGATE_CC_PATH, "r") as f:
            current_cc = f.read().strip()
        
        response = {
            "status": "success",
            "current_cc": current_cc
        }
        
        print(json.dumps(response, indent=4))
        
    except PermissionError:
        print(json.dumps({
            "status": "error", 
            "message": "Permission denied. Try running as root."
        }))
    except Exception as e:
        print(json.dumps({
            "status": "error", 
            "message": "Could not read delegate_cc", 
            "details": str(e)
        }))

if __name__ == "__main__":
    main()