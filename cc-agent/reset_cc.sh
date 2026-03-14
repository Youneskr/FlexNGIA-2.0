#!/bin/bash

echo "reno" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc > /dev/null
echo "Resetting TCP congestion control to 'reno' and unloading llm_cc_v modules..."

# Find all loaded modules starting with llm_cc_v
lsmod | awk '{print $1}' | grep '^llm_cc_v' | while read mod; do
    echo "Unloading $mod..."
    sudo rmmod "$mod" && echo "✓ $mod unloaded" || echo "✗ Failed to unload $mod"
done

# Clean workspace
sudo rm -rf agent/workspace
mkdir -p agent/workspace

echo "Workspace cleaned."