import sys
import os
import time
from scapy.all import sniff, IP, TCP

initial_time = None


def get_relative_time(pkt_time):
    global initial_time

    if initial_time is None:
        initial_time = pkt_time
        return 0.0

    return pkt_time - initial_time


def packet_handler(packet):
    global output_file

    if IP not in packet or TCP not in packet:
        return

    ip = packet[IP]
    tcp = packet[TCP]

    if ip.src != "10.0.0.1" or ip.dst != "10.0.0.2":
        return

    seq = tcp.seq
    relative_time = get_relative_time(packet.time)

    output_file.write(f"{relative_time:.6f}\t{seq}\n")
    output_file.flush()


def main():
    global output_file

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output_folder>")
        sys.exit(1)

    output_folder = sys.argv[1]
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "tcp_seq_log")

    try:
        output_file = open(output_path, "w")
    except IOError as e:
        print(f"Error opening output file: {e}")
        sys.exit(1)

    interface = "client-wlan0"
    bpf_filter = "tcp and src host 10.0.0.1 and dst host 10.0.0.2"

    print(f"Listening on {interface}... Logging to {output_path}")

    sniff(
        iface=interface,
        filter=bpf_filter,
        prn=packet_handler,
        store=False
    )


if __name__ == "__main__":
    main()