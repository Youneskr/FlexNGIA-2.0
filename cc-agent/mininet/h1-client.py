import socket
import struct
import time
import sys

# Configuration matches your Mininet topology
TARGET_IP = "10.0.0.2"  # IP of h2
TARGET_PORT = 5000
TCP_MONITOR_OPTION = 150
CHUNK_SIZE = 1024 * 32  # 32KB chunks
TEST_DURATION = 200     # Duration in seconds

def start_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[*] Connecting to {TARGET_IP}:{TARGET_PORT}...")
        sock.connect((TARGET_IP, TARGET_PORT))
        print("[*] Connected!")

        # --- ENABLE KERNEL MONITOR ---
        # Pack '1' as a 4-byte integer to enable Option 150
        val = struct.pack("i", 1)
        sock.setsockopt(socket.IPPROTO_TCP, TCP_MONITOR_OPTION, val)
        print(f"[*] Setsockopt {TCP_MONITOR_OPTION} enabled. Kernel is tracing.")

        # --- DATA FLOOD (TIME BASED) ---
        print(f"[*] Sending continuous traffic for {TEST_DURATION} seconds...")
        
        full_chunk = b'A' * CHUNK_SIZE
        total_bytes = 0
        start_time = time.time()
        
        # Loop until the difference between current time and start time exceeds duration
        while (time.time() - start_time) < TEST_DURATION:
            sock.sendall(full_chunk)
            total_bytes += CHUNK_SIZE
            
        elapsed = time.time() - start_time
        mbits = (total_bytes * 8) / 1_000_000
        
        print(f"[*] Done! Sent {total_bytes} bytes ({mbits:.2f} Mbits) in {elapsed:.2f} seconds.")
        print("[*] Closing connection.")

    except KeyboardInterrupt:
        print("\n[*] Interrupted by user.")
    except ConnectionRefusedError:
        print(f"[!] Connection refused. Is server.py running on {TARGET_IP}?")
    except OSError as e:
        print(f"[!] OS Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    start_flood()