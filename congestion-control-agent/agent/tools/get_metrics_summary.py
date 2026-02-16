import pandas as pd
import os
import sys
import json
import glob

# Path to results folder (relative to this script)
# agent/tools/ -> results/
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'results')

def get_latest_csv():
    """Finds the most recently modified CSV file in results/"""
    if not os.path.exists(RESULTS_DIR):
        return None
    
    list_of_files = glob.glob(os.path.join(RESULTS_DIR, '*.csv'))
    if not list_of_files:
        return None
        
    return max(list_of_files, key=os.path.getmtime)

def main():
    csv_file = get_latest_csv()
    
    if not csv_file:
        print(json.dumps({"error": "No active log file found."}))
        sys.exit(1)

    try:
        # Read the file (even if it is currently open/writing)
        df = pd.read_csv(csv_file)
        
        # Check if we have enough data
        if df.empty or len(df) < 5:
            print(json.dumps({"status": "waiting_for_data", "file": os.path.basename(csv_file)}))
            return

        # Calculate Statistics
        stats = {
            "status": "success",
            "file": os.path.basename(csv_file),
            "data_points": len(df),
            "metrics": {
                "cwnd": {
                    "avg": round(df['CWND'].mean(), 2),
                    "std": round(df['CWND'].std(), 2),
                    "min": int(df['CWND'].min()),
                    "max": int(df['CWND'].max())
                },
                "rate_mbps": {
                    "avg": round(df['RATE_MBPS'].mean(), 2),
                    "std": round(df['RATE_MBPS'].std(), 2),
                    "min": round(df['RATE_MBPS'].min(), 2),
                    "max": round(df['RATE_MBPS'].max(), 2),
                    "current": int(df['RATE_MBPS'].iloc[-1]) # The most recent value
                },
                "rtt_ms": {
                    "avg": round(df['RTT_MS'].mean(), 2),
                    "std": round(df['RTT_MS'].std(), 2),
                    "min": round(df['RTT_MS'].min(), 2),
                    "max": round(df['RTT_MS'].max(), 2),
                    "current": int(df['RTT_MS'].iloc[-1]) # The most recent value
                }
            }
        }
        
        # Output strictly JSON for the agent
        print(json.dumps(stats, indent=4))

    except Exception as e:
        # Handle read errors (e.g., if file is being written to at exact same moment)
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()