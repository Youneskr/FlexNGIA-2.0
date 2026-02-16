import sys
import os

# 1. Setup paths
# Get the directory where this script is located (agent/)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add agent/ to sys.path to find graph_brain.py
sys.path.append(current_dir)
# Add parent (mininet/) to sys.path so graph_brain can find 'agent.tools'
sys.path.append(os.path.dirname(current_dir))

try:
    # 2. Import the graph
    # We use a direct import since we are in the same folder
    from graph_brain import app
    
    output_file = "agent_architecture.png"
    print(f"[*] Generating graph visualization to '{output_file}'...")

    # 3. Generate Image
    # This returns the PNG binary data
    png_bytes = app.get_graph().draw_mermaid_png()

    # 4. Save to disk
    with open(output_file, "wb") as f:
        f.write(png_bytes)
    
    print(f"[*] Success! Saved to {os.path.join(current_dir, output_file)}")

except ImportError as e:
    print(f"[!] Import Error: {e}")
    print("    Ensure you are in the 'agent' folder and 'graph_brain.py' exists.")
except Exception as e:
    print(f"[!] Error: {e}")
    print("    Note: You might need to install 'grandalf' or use a mermaid viewer if PNG generation fails internally.")