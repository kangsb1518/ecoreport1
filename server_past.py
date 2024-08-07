import socket
import psycopg2

# 서버 설정 (호스트와 포트)
HOST = 'localhost'
PORT = 8080  # 소켓 통신 포트

# PostgreSQL 데이터베이스에 테이블을 생성하는 함수
def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                time FLOAT,
                a FLOAT,
                b FLOAT,
                result FLOAT
            )
        """)
    conn.commit()

# 데이터베이스에 데이터를 삽입하는 함수
def insert_data(conn, data):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sensor_data (time, a, b, result) VALUES (%s, %s, %s, %s)
        """, data)
    conn.commit()

# 서버 시작 함수
def start_server():
    try:
        # PostgreSQL 데이터베이스에 연결
        conn = psycopg2.connect(
            dbname="watertest", 
            user="postgres",  # postgres 사용자로 변경
            password="admin",  # 올바른 비밀번호 설정
            host="localhost",
            port=5432  # PostgreSQL 기본 포트 설정
        )
        # 테이블 생성
        create_table(conn)
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to the database: {e}")
        return

    # 서버 소켓 객체 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            # 클라이언트 연결 대기
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            try:
                while True:
                    # 데이터 수신
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    # 수신한 데이터를 디코딩하고 튜플로 변환
                    data_decoded = data.decode()
                    data_tuple = tuple(map(float, data_decoded.split(',')))
                    # 데이터를 데이터베이스에 삽입
                    insert_data(conn, data_tuple)
                    print(f"Received and inserted: {data_tuple}")
            finally:
                # 클라이언트 소켓 닫기
                client_socket.close()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        # 서버 소켓과 데이터베이스 연결 닫기
        server_socket.close()
        conn.close()

# 메인 함수
def main():
    start_server()

if __name__ == '__main__':
    main()