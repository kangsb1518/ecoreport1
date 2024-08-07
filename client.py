import socket
import random
import time
from datetime import datetime

# Server configuration
SERVER_HOST = '192.168.0.125'
SERVER_PORT = 8080

def generate_data():
    """Generate random sensor data."""
    flow = round(random.uniform(0, 100), 2)
    impuritiesA = round(random.uniform(0, 10), 2)
    impuritiesB = round(random.uniform(0, 10), 2)
    time_str = datetime.now().isoformat()
    return flow, impuritiesA, impuritiesB, time_str


def main():
    """Main function to send data to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to server.")

        try:
            while True:
                flow, impuritiesA, impuritiesB, time_str = generate_data()
                data = f"{flow},{impuritiesA},{impuritiesB},{time_str}"
                client_socket.sendall(data.encode())
                print(f"Sent: {data}")
                time.sleep(1)  # Send data every second
        except KeyboardInterrupt:
            print("Client stopped.")


if __name__ == '__main__':
    main()