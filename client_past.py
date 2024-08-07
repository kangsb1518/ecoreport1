import socket
import time
import pandas as pd
import numpy as np

from datetime import datetime #관측 시간 찍기위해 추가

# 서버의 호스트와 포트 설정
HOST = 'localhost'
PORT = 8080

# 임의의 데이터를 생성하는 함수
def generate_random_data():
    df = pd.DataFrame(np.random.rand(200, 3), columns=['flow', 'impurities1', 'impurities2'])
    df['time'] = [datetime.now().strftime('%Y-%m-%d %H:%M:%S') for _ in range(200)]
    return df[['flow', 'impurities1', 'impurities2', 'time']]

# 데이터를 서버로 보내는 함수
def send_data(client_socket, data_frame):
    try:
        for index, row in data_frame.iterrows():
            # 데이터를 문자열로 변환하여 전송
            data = ','.join(map(str, row.values))
            client_socket.sendall(data.encode())
            print(f"Sent: {data}")

            # 1초 대기시간 (데이터 전송 간격)
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

# 클라이언트 시작 함수
def start_client():
    # 소켓 객체 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 서버에 연결
        client_socket.connect((HOST, PORT))
        # 임의 데이터 생성
        data_frame = generate_random_data()
        # 데이터를 서버로 전송
        send_data(client_socket, data_frame)

    except KeyboardInterrupt:
        print("Client stopped.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 소켓 닫기
        client_socket.close()

# 메인 함수
def main():
    start_client()

if __name__ == '__main__':
    main()