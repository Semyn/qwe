import socket

HOST = '127.0.0.1'
PORT = 65432

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print('Ожидание клиента...')
        conn, addr = s.accept()
        with conn:
            print('Соединено с', addr)

            filename = conn.recv(1024).decode()
            print(f'Получен запрос на передачу файла: {filename}')

            confirm = input('Передать файл? (y/n): ')
            if confirm.lower() != 'y':
                conn.sendall('Отказ')
                print('Передача отменена.')
                return
            else:
                conn.sendall('Готово к передаче')

            response = conn.recv(1024).decode()
            if response != 'Начать':
                print('Передача не началась')
                return

            with open(filename, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)

            print('Файл получен успешно.')

            conn.sendall('Передача завершена успешно')