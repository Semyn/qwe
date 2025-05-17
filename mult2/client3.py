import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            message = input()
            sock.send(message.encode())
    except KeyboardInterrupt:
        sock.close()

if __name__ == '__main__':
    main()