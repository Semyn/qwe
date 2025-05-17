import socket
import os

HOST = '127.0.0.1'
PORT = 65432

def client():
    filename = input('Введите имя файла для отправки: ')
    if not os.path.isfile(filename):
        print('Файл не найден.')
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(filename.encode())


        response = s.recv(1024).decode()
        if response == 'Отказ':
            print('Передача отклонена сервером.')
            return
        elif response == 'Готово к передаче':
            confirm = input('Сервер готов принять файл. Начать передачу? (y/n): ')
            if confirm.lower() != 'y':
                print('Передача отменена.')
                return
            s.sendall('Начать')


            with open(filename, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    s.sendall(data)


            final_response = s.recv(1024).decode()
            if final_response == 'Передача завершена успешно':
                print('Файл успешно передан.')
            else:
                print('Произошла ошибка при передаче.')
        else:
            print('Неверный ответ от сервера.')