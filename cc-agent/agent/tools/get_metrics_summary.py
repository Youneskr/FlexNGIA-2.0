import pandas as pd
import os
import sys
import json
import glob

# Path to results folder (relative to this script)
# agent/tools/ -> results/
RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "results"
)

def get_latest_csv():
    """Find the most recent results/<session>/<session>.csv file"""

    if not os.path.exists(RESULTS_DIR):
        return None

    csv_files = []

    for d in os.listdir(RESULTS_DIR):
        session_dir = os.path.join(RESULTS_DIR, d)

        if not os.path.isdir(session_dir):
            continue

        csv_path = os.path.join(session_dir, f"{d}.csv")

        if os.path.exists(csv_path):
            csv_files.append(csv_path)

    if not csv_files:
        return None

    return max(csv_files, key=os.path.getmtime)


def main():
    csv_file = get_latest_csv()

    if not csv_file:
        print(json.dumps({"status": "error", "message": "No active log file found"}))
        sys.exit(1)

    try:
        df = pd.read_csv(csv_file)

        # Not enough data yet
        if df.empty or len(df) < 5:
            print(json.dumps({
                "status": "waiting_for_data",
                "file": os.path.basename(csv_file)
            }))
            return

        stats = {
            "status": "success",
            "file": os.path.basename(csv_file),
            "data_points": int(len(df)),
            "metrics": {
                "cwnd": {
                    "avg": float(round(df["CWND"].mean(), 2)),
                    "std": float(round(df["CWND"].std(), 2)),
                    "min": int(df["CWND"].min()),
                    "max": int(df["CWND"].max())
                },
                "rate_mbps": {
                    "avg": float(round(df["RATE_MBPS"].mean(), 2)),
                    "std": float(round(df["RATE_MBPS"].std(), 2)),
                    "min": float(round(df["RATE_MBPS"].min(), 2)),
                    "max": float(round(df["RATE_MBPS"].max(), 2)),
                    "current": float(df["RATE_MBPS"].iloc[-1])
                },
                "rtt_ms": {
                    "avg": float(round(df["RTT_MS"].mean(), 2)),
                    "std": float(round(df["RTT_MS"].std(), 2)),
                    "min": float(round(df["RTT_MS"].min(), 2)),
                    "max": float(round(df["RTT_MS"].max(), 2)),
                    "current": float(df["RTT_MS"].iloc[-1])
                },
                "lost_segments": {
                    "avg": float(round(df["RTX_TOT"].mean(), 2)),
                    "std": float(round(df["RTX_TOT"].std(), 2)),
                    "min": int(df["RTX_TOT"].min()),
                    "max": int(df["RTX_TOT"].max()),
                    "current": int(df["RTX_TOT"].iloc[-1])
                }
            }
        }

        # Output JSON for the agent
        print(json.dumps(stats, indent=4))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": str(e)
        }))


if __name__ == "__main__":
    main()