import socket
import psycopg2

# PostgreSQL Database configuration
DATABASE = 'waterCondition'  # Replace with your existing database name
USER = 'postgres'  # Replace with your PostgreSQL username
PASSWORD = 'admin'  # Replace with your PostgreSQL password
HOST_DB = 'localhost'  # Replace with your PostgreSQL server host if not local
PORT_DB = 5432  # Replace with your PostgreSQL port if different

# TCP Server configuration
HOST = '0.0.0.0'  # Listens on all network interfaces
PORT = 8080


def connect_to_database():
    """Connect to the existing PostgreSQL database and return the connection and cursor."""
    try:
        conn = psycopg2.connect(
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST_DB,
            port=PORT_DB
        )
        cursor = conn.cursor()
        print("Connection to existing database established successfully.")
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None


def insert_data(cursor, flow, impurities1, impurities2, time_str):
    """Insert data into the 'realtime' table."""
    insert_query = """
    INSERT INTO realtime (flow, impurities1, impurities2, time)
    VALUES ( %s, %s, %s, %s);
    """
    try:
        cursor.execute(insert_query, (flow, impurities1, impurities2, time_str))
        cursor.connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        cursor.connection.rollback()


def handle_client(client_socket, cursor):
    """Handle incoming TCP connections and process data sent by the Raspberry Pi."""
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            flow, impurities1, impurities2, time_str = data.split(',')
            insert_data(cursor, float(flow), float(impurities1), float(impurities2), time_str)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    """Start the server to handle TCP connections."""
    conn, cursor = connect_to_database()
    if cursor:
        # No need to create table as it already exists

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"Server listening on {HOST}:{PORT}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connected by {addr}")
                handle_client(client_socket, cursor)

        # Close the database connection
        cursor.close()
        conn.close()


def main():
    start_server()


if __name__ == '__main__':
    main()