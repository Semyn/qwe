import socket

HOST = 'localhost'
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Подключено к серверу. Ожидайте начала игры.")
        while True:
            data = s.recv(1024).decode()
            if not data:
                break
            if data.startswith('WELCOME'):
                print("Игра началась!")

            elif data.startswith('MOVE'):
                move_number = int(data.split()[1])
                print(f"Компьютер сделал ход: {move_number}")
            elif data.startswith('LOSE'):
                print("Вы проиграли.")
                break
            elif data.startswith('DRAW'):
                print("Ничья.")
                break
            elif data.startswith('EXIT'):
                print("Игра завершена.")
                break
            elif data.startswith('YOUR_TURN'):
                move = input("Ваш ход (0-8): ")
                s.send(f'MOVE {move}\n'.encode())
        print("Конец игры.")

if __name__ == '__main__':
    main()