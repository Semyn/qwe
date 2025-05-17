import socket
import threading

HOST = 'localhost'
PORT = 65432

board = [' ' for _ in range(9)]
current_player = 'X'
game_active = True

def print_board():
    print(f"{board[0]}|{board[1]}|{board[2]}")
    print("-+-+-")
    print(f"{board[3]}|{board[4]}|{board[5]}")
    print("-+-+-")
    print(f"{board[6]}|{board[7]}|{board[8]}")

def check_win(player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in cond) for cond in win_conditions)

def check_draw():
    return all(space != ' ' for space in board)

def handle_server(conn, addr):
    global game_active, current_player
    print('Client connected', addr)
    conn.send('WELCOME\n'.encode())

    while game_active:
        if current_player == 'X':

            print_board()
            move = input("Ваш ход (0-8, или 'exit' для выхода): ")
            if move.lower() == 'exit':
                conn.send('EXIT\n'.encode())
                break
            if move.isdigit() and int(move) in range(9):
                idx = int(move)
                if board[idx] == ' ':
                    board[idx] = 'X'
                    if check_win('X'):
                        print_board()
                        print("Вы выиграли!")
                        conn.send('LOSE\n'.encode())
                        break
                    elif check_draw():
                        print_board()
                        print("Ничья!")
                        conn.send('DRAW\n'.encode())
                        break
                    else:
                        conn.send(f'MOVE {move}\n'.encode())
                        current_player = 'O'
                else:
                    print("Клетка занята")
            else:
                print("Некорректный ввод")
        else:

            print('Ожидание хода другого игрока...')
            data = conn.recv(1024).decode()
            if not data:
                break
            if data.startswith('MOVE'):
                move = int(data.split()[1])
                if board[move] == ' ':
                    board[move] = 'O'
                    if check_win('O'):
                        print_board()
                        print("Вы проиграли!")
                        break
                    elif check_draw():
                        print_board()
                        print("Ничья!")
                        break
                    else:
                        current_player = 'X'
            elif data.startswith('EXIT'):
                print("Игрок вышел из игры.")
                break
    conn.close()

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен и слушает {HOST}:{PORT}")
        conn, addr = s.accept()
        handle_server(conn, addr)
        print("Игра завершена.")

if __name__ == '__main__':
    server()