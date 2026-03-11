#!/bin/bash

echo "reno" | sudo tee /sys/module/tcp_proxy/parameters/delegate_cc > /dev/null
echo "Resetting TCP congestion control to 'Reno' and unloading llm_cc_v modules..."

sysctl net.ipv4.tcp_available_congestion_control | tr " " "\n" | grep -oP "llm_cc_v\K[0-9]+" | while read id; do
    echo "Unloading llm_cc_v${id}..."
    sudo rmmod llm_cc_v${id} && echo "✓ llm_cc_v${id} unloaded" || echo "✗ Failed to unload llm_cc_v${id}"
done

sudo rm -rf agent/workspace
mkdir -p agent/workspace