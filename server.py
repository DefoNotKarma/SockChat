import socket
import threading

def find_open_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
    
 
PORT = 5050 or find_open_port()
SERVER = socket.gethostbyname(socket.gethostname())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "!dsc"

server_socket.bind(ADDR)

clients = []

def handle_client(conn, addr):
    # getting username in same variable to save space
    username =  conn.recv(HEADER).decode(FORMAT)
    if username:
        username = int(username.strip())
        username = conn.recv(username).decode(FORMAT)
        if not username:
            username = addr
    clients.append((username, addr))
    print(clients)
    print(f"[New Connection] : {addr} connected. Welcome {username}")
    connected = True

    while connected:
        get_user_msg_len = conn.recv(HEADER).decode(FORMAT)


        if get_user_msg_len:
            get_user_msg_len = int(get_user_msg_len.strip())
            message = conn.recv(get_user_msg_len).decode(FORMAT)
            
            if message == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{username}]: {message}")

    print(f"\n{username} disconnected")

    conn.close()


def start_server():
    server_socket.listen()
    print(f"[Listening] IP = {SERVER}, {PORT=}")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] : {threading.active_count() - 1}")

print("STARTING SERVER...")
start_server()