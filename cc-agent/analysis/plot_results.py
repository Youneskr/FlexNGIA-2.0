import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_metric(df, x_col, y_col, title, ylabel, color, output_dir, file_suffix):
    """
    Plots raw data without smoothing.
    """
    plt.figure(figsize=(10, 6))
    
    # Plotting Logic:
    # linewidth=1.0 makes the line sharper.
    # linestyle='-' connects points with straight lines (no spline smoothing).
    # alpha=0.9 makes it opaque and clear.
    plt.plot(df[x_col], df[y_col], label=y_col, color=color, linewidth=1.0, linestyle='-', alpha=0.9)
    
    # Styling
    plt.title(title, fontsize=14)
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    # Construct full output path
    output_path = os.path.join(output_dir, file_suffix)
    
    # Save and close
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"    -> Saved: {output_path}")

def main():
    # 1. Check Arguments
    if len(sys.argv) < 2:
        print("Usage: python3 analysis/plot_results.py <path_to_csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"[!] Error: File {csv_file} not found.")
        sys.exit(1)

    # 2. Setup Directory Structure
    # Input: results/0.csv
    # Desired Output: analysis/images/0/
    
    # Get the "0" from "results/0.csv"
    run_id = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Create the target folder path
    # We go up one level from 'analysis/plot_results.py' location context if needed,
    # but simpler is to stick to relative paths from root.
    output_dir = os.path.join("analysis", "images", run_id)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[*] Created directory: {output_dir}")

    # 3. Read CSV Data
    try:
        print(f"[*] Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"[!] Error reading CSV: {e}")
        sys.exit(1)

    print(f"[*] Generating plots in {output_dir}...")

    # --- PLOT 1: Congestion Window (CWND) ---
    plot_metric(
        df, 
        x_col='TIME', 
        y_col='CWND', 
        title='Congestion Window (Raw)', 
        ylabel='CWND (Packets)', 
        color='#1f77b4', # Standard Blue
        output_dir=output_dir,
        file_suffix='cwnd.png'
    )

    # --- PLOT 2: Sending Rate (Throughput) ---
    plot_metric(
        df, 
        x_col='TIME', 
        y_col='RATE_MBPS', 
        title='Throughput (Raw)', 
        ylabel='Rate (Mbps)', 
        color='#2ca02c', # Standard Green
        output_dir=output_dir,
        file_suffix='rate.png'
    )

    # --- PLOT 3: Round Trip Time (RTT) ---
    plot_metric(
        df, 
        x_col='TIME', 
        y_col='RTT_MS', 
        title='Round Trip Time (Raw)', 
        ylabel='RTT (ms)', 
        color='#d62728', # Standard Red
        output_dir=output_dir,
        file_suffix='rtt.png'
    )
    
    # --- PLOT 4: Combined Dashboard ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
    
    # CWND Subplot
    ax1.plot(df['TIME'], df['CWND'], color='#1f77b4', linewidth=1.0)
    ax1.set_ylabel('CWND')
    ax1.set_title('Connection Overview (Raw Data)')
    ax1.grid(True, alpha=0.5)

    # Rate Subplot
    ax2.plot(df['TIME'], df['RATE_MBPS'], color='#2ca02c', linewidth=1.0)
    ax2.set_ylabel('Mbps')
    ax2.grid(True, alpha=0.5)

    # RTT Subplot
    ax3.plot(df['TIME'], df['RTT_MS'], color='#d62728', linewidth=1.0)
    ax3.set_ylabel('RTT (ms)')
    ax3.set_xlabel('Time (s)')
    ax3.grid(True, alpha=0.5)

    dashboard_path = os.path.join(output_dir, "dashboard.png")
    plt.savefig(dashboard_path, dpi=300)
    plt.close()
    print(f"    -> Saved: {dashboard_path}")

if __name__ == "__main__":
    main()