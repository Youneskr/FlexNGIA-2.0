#!/bin/bash

# Configuration
TOPO_FILE="mininet/topo.py"
RESULTS_DIR="results"
TRACE_DIR="/sys/kernel/debug/tracing"

# 1. Check for Root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run as root (sudo ./run_test.sh)"
  exit
fi

# 2. Results Directory and Auto-Increment Logic
# Create directory if it doesn't exist
if [ ! -d "$RESULTS_DIR" ]; then
    echo "[*] Creating results directory..."
    mkdir -p "$RESULTS_DIR"
fi

# Find the next available filename (0.csv, 1.csv, ...)
count=0
while [ -f "$RESULTS_DIR/$count.csv" ]; do
    ((count++))
done

LOG_FILE="$RESULTS_DIR/$count.csv"
echo "[*] New log file will be: $LOG_FILE"

# This runs automatically when the script exits or is killed (Ctrl+C)
cleanup() {
    echo ""
    echo "[*] Stopping Tracer and cleaning up..."
    
    # 1. Stop the kernel tracer immediately
    echo 0 > $TRACE_DIR/tracing_on
    
    # 2. Kill the specific background logger we started
    if [ ! -z "$LOGGER_PID" ]; then
        kill $LOGGER_PID 2>/dev/null
    fi

    # 3. AGGRESSIVE CLEANUP: Find and kill ANY lingering cat processes 
    # reading the trace_pipe. This ensures your 'ps aux' is clean.
    pkill -f "cat $TRACE_DIR/trace_pipe"
    
    echo "[*] Done. Logs saved to $LOG_FILE"
}

# Run 'cleanup' on EXIT, Ctrl+C (SIGINT), or Kill (SIGTERM)
trap cleanup EXIT INT TERM

# -------------------------------

# 3. Cleanup Mininet
echo "[*] Cleaning up previous Mininet sessions..."
mn -c > /dev/null 2>&1

# 4. Configure Kernel Tracing
echo "[*] Configuring Kernel Tracing..."
echo 0 > $TRACE_DIR/tracing_on                 # Pause tracing
echo > $TRACE_DIR/trace                        # Clear old logs
echo 1 > $TRACE_DIR/events/tcp/tcp_monitor_log/enable # Enable event
echo 1 > $TRACE_DIR/tracing_on                 # Start tracing

# 5. Start Background Logger
echo "[*] Capturing parsed CSV logs to $LOG_FILE"
# Pipe raw trace -> python parser -> CSV file
cat $TRACE_DIR/trace_pipe | python3 helpers/log_parser.py > "$LOG_FILE" &
LOGGER_PID=$!

# 6. Run the Mininet Topology
echo "[*] Starting Topology. Press Ctrl+D in Mininet CLI to exit."
echo "---------------------------------------------------------"
python3 $TOPO_FILE 2>&1 | grep -v "sch_htb"
echo "---------------------------------------------------------"

# SIGNAL TERMINATION TO AGENT
echo "[*] Signaling session termination..."
touch "$RESULTS_DIR/$count.terminated"

# --- GENERATE PLOTS AUTOMATICALLY ---
echo "[*] Generating plots for $LOG_FILE..."
python3 analysis/plot_results.py "$LOG_FILE"