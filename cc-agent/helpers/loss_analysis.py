#!/usr/bin/env python3

from collections import defaultdict
import os
import sys

# -------------------------------------------------
# Input / Output paths
# -------------------------------------------------

# Expect run directory as argument
if len(sys.argv) != 2:
    print("Usage: loss_analysis.py <run_directory>")
    sys.exit(1)

base_path = sys.argv[1]

input_file = os.path.join(base_path, "tcp_seq_log")
output_file = os.path.join(base_path, "loss_stats")

# Time slot duration (seconds)
SLOT_DURATION = 10.0

# -------------------------------------------------
# Validate input
# -------------------------------------------------

if not os.path.exists(input_file):
    print(f"[!] Input file not found: {input_file}")
    sys.exit(1)

# -------------------------------------------------
# Read tcp_seq_log
# -------------------------------------------------

with open(input_file, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    print("[!] tcp_seq_log is empty")
    sys.exit(0)

# Parse lines
entries = [(float(t), seq) for t, seq in (line.split('\t') for line in lines)]

# -------------------------------------------------
# Group packets into time slots
# -------------------------------------------------

slots = defaultdict(list)

for time_val, seq in entries:
    slot_index = int(time_val // SLOT_DURATION) + 1
    slots[slot_index].append(seq)

# -------------------------------------------------
# Compute statistics
# -------------------------------------------------

with open(output_file, "w") as out:

    for slot_num in sorted(slots.keys()):
        seqs = slots[slot_num]

        counts = defaultdict(int)
        for s in seqs:
            counts[s] += 1

        unique_segments = sum(1 for c in counts.values() if c >= 1)
        retransmissions = sum(c - 1 for c in counts.values() if c > 1)

        total_transmissions = unique_segments + retransmissions

        ratio = retransmissions / unique_segments if unique_segments > 0 else 0.0

        out.write(
            f"{slot_num}\t{unique_segments}\t{retransmissions}\t"
            f"{total_transmissions}\t{ratio*100:.2f}\n"
        )