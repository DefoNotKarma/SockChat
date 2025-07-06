import socket
import threading
from datetime import datetime
import bz2
import json


def find_open_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
    
 
PORT = 5050 or find_open_port()
SERVER = socket.gethostbyname(socket.gethostname())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
HEADER = 8
LOG_HEADER = 64
DISCONNECT_MESSAGE = "!dsc"



server_socket.bind(ADDR)

messages = []
clients = {}

def send_chatlogs(conn, data):

    data_size = str(len(data)).encode(FORMAT)
    data_size += b' ' * (LOG_HEADER - len(data_size))
    conn.send(data_size)
    conn.send(data)

def broardcast_new_messages():
    pass


def handle_client(conn, addr):

    # getting username in same variable to save space
    username =  conn.recv(HEADER).decode(FORMAT)
    if username:
        username = int(username.strip())
        username = conn.recv(username).decode(FORMAT)
        if not username:
            username = addr

    clients.append(addr)
    print(f"[New Connection] : {addr} connected. Welcome {username}.")

    # send chat history
    data = json.dumps(messages).encode(FORMAT)
    data = bz2.compress(data)

    send_chatlogs(conn, data)



    connected = True

    while connected:
        try:
            get_user_msg_len = conn.recv(HEADER).decode(FORMAT)

            if get_user_msg_len:
                get_user_msg_len = int(get_user_msg_len.strip())
                message = conn.recv(get_user_msg_len).decode(FORMAT)

                # maintain messages sent 
                message_log = {"username" : username,
                                "message" : message,
                                "time" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                
                messages.append(message_log)
                
                if message == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"[{username}]: {message}")
        except ConnectionResetError as err:
            print(f"\n{username} severed the connection forcefully.")
            connected = False


    print(f"{username} disconnected.\n")
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