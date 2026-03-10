import socket
import sys

# Listen on all interfaces
IP = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow reusing the address to avoid "Address already in use" errors
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((IP, PORT))
    server.listen(1)
    print(f"[*] Server listening on {IP}:{PORT}")

    try:
        # Accept only ONE connection
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        total_bytes = 0
        while True:
            data = client.recv(BUFFER_SIZE)
            if not data:
                break
            total_bytes += len(data)
        
        # Print summary
        print(f"[*] Connection closed by client.")
        print(f"[*] Total Received: {total_bytes / (1024*1024):.2f} MB")
        
        # Close client socket
        client.close()

    except KeyboardInterrupt:
        print("\n[*] Stopping server manually.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        # Close server socket and exit
        server.close()
        print("[*] Server terminated.")
        sys.exit(0)

if __name__ == "__main__":
    start_server()