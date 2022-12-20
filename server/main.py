import threading
import socket
import json
import time

# Адрес и порт, на котором сервер будет слушать подключения
SERVER_ADDRESS = ('localhost', 8000)

# Максимальное количество одновременных подключений
MAX_CONNECTIONS = 2

connections = []
current_q = 0


def Send(conn, data):
    conn.send(json.dumps(data).encode())


def Listen(conn):
    global current_q
    while True:
        data = conn.recv(1024).decode()
        data = json.loads(data)

        if list(data.keys())[0] == 'sat':
            current_q = list(data.values())[0]
        if list(data.keys())[0] == 'usr':
            coords = {'coords': current_q}
            Send(conn, coords)

        time.sleep(0.1)


# Функция, которая обрабатывает каждое новое подключение
def handle_connection():
    # Обрабатываем подключение
    while True:
        # Принимаем новое подключение
        conn, addr = server_sock.accept()
        print(f'Получено новое подключение от {addr}')
        connections.append(conn)
        # Создаем новый поток для обработки подключения
        threading.Thread(target=Listen, args=(conn,)).start()


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    # Создаем серверный сокет

    server_sock.bind(SERVER_ADDRESS)
    server_sock.listen(MAX_CONNECTIONS)

    # Бесконечный цикл для приема новых подключений

    thread1 = threading.Thread(target=handle_connection)
    thread1.start()


if __name__ == '__main__':
    main()
