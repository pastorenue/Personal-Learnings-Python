import os
import signal
import socket
import json
import time
import hashlib
from pathlib import Path
from threading import Thread
from typing import Dict, Set

class FileMonitor:
    def __init__(self, directory, watched_files=None, host='localhost', port=5000):
        self.directory = Path(directory)
        self.host = host
        self.port = port
        self.running = False
        self.known_files = set()
        self.watched_files = set(watched_files) if watched_files else set()
        self.file_hashes: Dict[str, str] = {}
        self.sock = None
        self.server_thread = None
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
    
    def set_file_hash_diff(self, prev_hash, current_hash):
        pass

    def handle_shutdown(self, signum, frame):
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
        if self.sock:
            self.sock.close()
    
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {filepath}: {e}")
            return ""

    def setup_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Listening for connections on {self.host}:{self.port}")
    
    def accept_connections(self):
        while self.running:
            try:
                client_socket, addr = self.sock.accept()
                print(f"New connection from {addr}")
                client_thread = Thread(target=self.handle_client, args=(client_socket,))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
    
    def handle_client(self, client_socket):
        try:
            while self.running:
                # Send current status to clients
                status = {
                    "type": "status",
                    "all_files": list(self.known_files),
                    "watched_files": {
                        str(file): self.file_hashes.get(str(file), "")
                        for file in self.watched_files
                    }
                }
                message = json.dumps(status)
                client_socket.send(f"{message}\n".encode())
                time.sleep(1)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def get_current_files(self) -> Set[str]:
        return set(
            str(f.relative_to(self.directory))
            for f in self.directory.rglob('*')
            if f.is_file()
        )
    
    def check_watched_files(self):
        """Check for changes in specifically watched files."""
        changes = []
        for file in self.watched_files:
            file_path = self.directory / file
            if file_path.exists():
                current_hash = self.calculate_file_hash(file_path)
                previous_hash = self.file_hashes.get(str(file))
                
                if previous_hash is None:
                    changes.append(f"Started watching {file}")
                    self.file_hashes[str(file)] = current_hash
                elif current_hash != previous_hash:
                    changes.append(f"Content changed in {file}")
                    self.file_hashes[str(file)] = current_hash
            else:
                if str(file) in self.file_hashes:
                    changes.append(f"Watched file {file} was deleted")
                    self.file_hashes.pop(str(file))
        
        return changes
    
    def check_for_changes(self):
        while self.running:
            try:
                current_files = self.get_current_files()
                
                # Check for new files
                new_files = current_files - self.known_files
                if new_files:
                    print(f"New files detected: {new_files}")
                    # Add any new files that match our watch list
                    for file in new_files:
                        if file in self.watched_files:
                            self.file_hashes[file] = self.calculate_file_hash(self.directory / file)
                
                # Check for deleted files
                deleted_files = self.known_files - current_files
                if deleted_files:
                    print(f"Files deleted: {deleted_files}")
                
                # Check watched files for content changes
                changes = self.check_watched_files()
                if changes:
                    for change in changes:
                        print(f"Change detected: {change}")
                
                 # Update known files
                self.known_files = current_files
                time.sleep(1)
                
            except Exception as e:
                print(f"Error checking for changes: {e}")
    
    def add_watch_file(self, filepath: str):
        """Add a file to the watch list."""
        relative_path = str(Path(filepath))
        self.watched_files.add(relative_path)
        file_path = self.directory / relative_path
        if file_path.exists():
            self.file_hashes[relative_path] = self.calculate_file_hash(file_path)
            print(f"Now watching {relative_path}")
        else:
            print(f"Warning: File {relative_path} doesn't exist yet, but will be watched when created")
    
    def remove_watch_file(self, filepath: str):
        """Remove a file from the watch list."""
        relative_path = str(Path(filepath))
        self.watched_files.discard(relative_path)
        self.file_hashes.pop(relative_path, None)
        print(f"Stopped watching {relative_path}")
    
    def start(self):
        self.running = True
        self.known_files = self.get_current_files()
        
        # Initialize hashes for watched files
        for file in self.watched_files:
            file_path = self.directory / file
            if file_path.exists():
                self.file_hashes[str(file)] = self.calculate_file_hash(file_path)
        
        # Start socket server
        self.setup_socket()
        self.server_thread = Thread(target=self.accept_connections)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Start monitoring
        self.check_for_changes()

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: script.py directory_to_monitor file1_to_watch [file2_to_watch ...]")
        sys.exit(1)
    
    directory = sys.argv[1]
    watch_files = sys.argv[2:]
    
    monitor = FileMonitor(directory, watch_files)
    print(f"Monitoring directory: {directory}")
    print(f"Watching files: {watch_files}")
    monitor.start()
