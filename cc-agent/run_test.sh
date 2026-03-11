#!/bin/bash
# set -e

# -------------------------------------------------
# Configuration
# -------------------------------------------------

TOPO_FILE="mininet/topo.py"
RESULTS_DIR="results"
TRACE_DIR="/sys/kernel/debug/tracing"

CLIENT_SCRIPT="mininet/h1-client.py"
SERVER_SCRIPT="mininet/h2-server.py"
SNIFFER_SCRIPT="helpers/tcp_seq_sniffer.py"

READY_FILE="/tmp/mininet_ready"
MININET_LOG="/tmp/mininet.log"

# -------------------------------------------------
# Root Check
# -------------------------------------------------

if [ "$EUID" -ne 0 ]; then
    echo "[!] Please run as root (sudo ./run_test.sh)"
    exit 1
fi

# -------------------------------------------------
# Prepare Results Directory
# -------------------------------------------------

mkdir -p "$RESULTS_DIR"

count=0
while [ -d "$RESULTS_DIR/$count" ]; do
    ((count++))
done

RUN_DIR="$RESULTS_DIR/$count"
mkdir -p "$RUN_DIR"

LOG_FILE="$RUN_DIR/$count.csv"

echo "[*] Run directory: $RUN_DIR"
echo "[*] CSV log file: $LOG_FILE"

# -------------------------------------------------
# Cleanup Handler
# -------------------------------------------------

cleanup() {

    echo ""
    echo "[*] Cleaning up experiment..."

    # Stop tracing
    echo 0 > "$TRACE_DIR/tracing_on" 2>/dev/null || true

    # Kill logger pipeline
    if [ -n "$LOGGER_PID" ]; then
        kill "$LOGGER_PID" 2>/dev/null || true
    fi

    # Kill any remaining trace_pipe readers
    pkill -f "trace_pipe" 2>/dev/null || true

    # Stop experiment processes
    [ -n "$SNIFFER_PID" ] && kill "$SNIFFER_PID" 2>/dev/null || true
    [ -n "$SERVER_PID_JOB" ] && kill "$SERVER_PID_JOB" 2>/dev/null || true
    [ -n "$MININET_PID" ] && kill "$MININET_PID" 2>/dev/null || true

    # Remove topology ready file
    rm -f "$READY_FILE"

    # Clean Mininet
    mn -c > /dev/null 2>&1 || true

    echo "[*] Cleanup complete"
}

trap cleanup EXIT INT TERM

# -------------------------------------------------
# Clean Previous Mininet
# -------------------------------------------------

echo "[*] Cleaning previous Mininet sessions..."
mn -c > /dev/null 2>&1
./reset_cc.sh > /dev/null 2>&1

# -------------------------------------------------
# Configure Kernel Tracing
# -------------------------------------------------

echo "[*] Configuring kernel tracing..."

echo 0 > "$TRACE_DIR/tracing_on"
echo > "$TRACE_DIR/trace"

echo 1 > "$TRACE_DIR/events/tcp/tcp_monitor_log/enable"
echo 1 > "$TRACE_DIR/tracing_on"

# -------------------------------------------------
# Start Trace Logger
# -------------------------------------------------

echo "[*] Starting trace logger..."

cat "$TRACE_DIR/trace_pipe" | python3 helpers/log_parser.py > "$LOG_FILE" &
LOGGER_PID=$!

# -------------------------------------------------
# Start Mininet Topology
# -------------------------------------------------

echo "[*] Starting Mininet topology..."

rm -f "$READY_FILE"

python3 "$TOPO_FILE" > "$MININET_LOG" 2>&1 &
MININET_PID=$!

# -------------------------------------------------
# Wait for Topology Ready
# -------------------------------------------------

echo "[*] Waiting for topology..."

while [ ! -f "$READY_FILE" ]; do
    sleep 0.2
done

echo "[*] Topology ready."

# -------------------------------------------------
# Detect Mininet Hosts
# -------------------------------------------------

CLIENT_PID=$(pgrep -f "mininet:client$")
SERVER_PID=$(pgrep -f "mininet:server$")

echo "[*] Client PID: $CLIENT_PID"
echo "[*] Server PID: $SERVER_PID"
sleep 2

# -------------------------------------------------
# Start Server
# -------------------------------------------------

echo "[*] Starting server..."

mnexec -a "$SERVER_PID" python3 "$SERVER_SCRIPT" \
    > /dev/null 2>&1 &
SERVER_PID_JOB=$!

sleep 2

# -------------------------------------------------
# Start TCP Sequence Sniffer
# -------------------------------------------------

echo "[*] Starting TCP sequence sniffer..."

mnexec -a "$CLIENT_PID" python3 "$SNIFFER_SCRIPT" "$RUN_DIR" \
    > /dev/null 2>&1 &
SNIFFER_PID=$!

sleep 2

# -------------------------------------------------
# Start Client
# -------------------------------------------------

echo "[*] Starting client..."

./clock.sh start
echo "0" > "./clock.log"

mnexec -a "$CLIENT_PID" python3 "$CLIENT_SCRIPT" \
    > /dev/null 2>&1

printf "\n" >> "./clock.log" && sudo ./clock.sh get >> "./clock.log"

echo "[*] Client finished."

# -------------------------------------------------
# Signal Experiment End
# -------------------------------------------------

./clock.sh clear
touch "$RUN_DIR/terminated"

# -------------------------------------------------
# Analyze TCP loss
# -------------------------------------------------

echo "[*] Computing TCP loss statistics..."

python3 helpers/loss_analysis.py "$RUN_DIR"


# -------------------------------------------------
# Generate Plots
# -------------------------------------------------

echo "[*] Generating plots..." 
python3 analysis/plot_results.py "$LOG_FILE" 


python3 helpers/generate_cc_periods.py "clock.log" "$RUN_DIR/cc_periods" 

rm -f "clock.log"

./reset_cc.sh > /dev/null 2>&1
echo "[*] Experiment finished."