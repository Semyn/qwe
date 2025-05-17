import socket
import threading

HOST = '127.0.0.1'
PORT = 12345


users = {
    'user1': 'pass1',
    'user2': 'pass2',
    'user3': 'pass3'
}

clients = {} 

def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                remove_client(client_socket)

def remove_client(client_socket):
    login = clients.get(client_socket)
    if login:
        print(f"{login} отключился.")
        del clients[client_socket]
    client_socket.close()

def handle_client(client_socket):
    try:

        client_socket.send('Введите логин: ')
        login = client_socket.recv(1024).decode().strip()
        client_socket.send('Введите пароль: ')
        password = client_socket.recv(1024).decode().strip()

        if login in users and users[login] == password:
            clients[client_socket] = login
            client_socket.send('Успешный вход!\n')
            print(f'{login} вошел в чат.')
            broadcast(f'{login} вошел в чат.\n'.encode(), client_socket)

            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                msg = f'{login}: {message.decode()}'
                print(msg)
                broadcast(msg.encode(), client_socket)
        else:
            client_socket.send('Неверные логин или пароль.\n')
            client_socket.close()
    except:
        remove_client(client_socket)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f'Сервер запущен на {HOST}:{PORT}')

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == '__main__':
    main()