import json
import socket
import signal
import sys


class FileMonitorClient:
    def __init__(self, host='localhost', port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    
    def receive_updates(self):
        try:
            while True:
                try:
                    data = self.sock.recv(4096).decode()
                    if not data:
                        print("Connection closed by server.")
                        break
                        
                    messages = data.strip().split('\n')
                    for message in messages:
                        try:
                            update = json.loads(message)
                            print(f"Received update: {update}")
                        except json.JSONDecodeError as json_err:
                            print(f"JSON decode error: {json_err}")
                            continue
                            
                except socket.error as sock_err:
                    print(f"Socket error: {sock_err}")
                    break
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("Closing socket.")
            self.sock.close()

    def shutdown(self):
        # Set up signal handlers
        def _down(signum, frame):
            print(f"\nReceived signal {signum}. Shutting down gracefully...")
            sys.exit(0)
            exit(0)

        signal.signal(signal.SIGINT, _down)
        signal.signal(signal.SIGTERM, _down)

if __name__ == "__main__":
    client = FileMonitorClient()
    client.receive_updates()
