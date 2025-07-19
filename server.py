import socket
import threading
from datetime import datetime
import bz2
import json
from queue import Queue


def find_open_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
    
 
PORT = find_open_port()

# to run scripts locally or over LAN
SERVER = socket.gethostbyname(socket.gethostname())

"""
to run scripts over a public network, uncomment the line under and
put your tailscale assigned IP in place.

"""
#SERVER = "100.x.y.z"



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
HEADER = 8
LOG_HEADER = 64
HEADER = 8
LOG_HEADER = 64
DISCONNECT_MESSAGE = "!dsc"
BLANK_HEADER = str(len("")).encode(FORMAT)
BLANK_HEADER += b' ' * (HEADER - len(BLANK_HEADER))


server_socket.bind(ADDR)

messages = []
message_queue = Queue()
thread_lock = threading.Lock()

clients = []

def send_chatlogs(conn, data):

    data_size = str(len(data)).encode(FORMAT)
    data_size += b' ' * (LOG_HEADER - len(data_size))
    conn.send(data_size)
    conn.send(data)

def broardcast_new_messages():
    while True:
        with thread_lock:
            addr, message = message_queue.get()

            print(f"{message=}, {message_queue=}", )
            if not message["message"]:
                continue

        message = json.dumps(message).encode(FORMAT)

        with thread_lock:
            for client in list(clients):
                try:
                    if client.getpeername() == addr:
                        continue
                    
                    data_size = str(len(message)).encode(FORMAT)
                    data_size += b' ' * (HEADER - len(data_size))
                    client.send(data_size)
                    client.send(message)
                except OSError:
                    print("[ALERT] Found disconnected client. Removing them")
                    clients.remove(client)


            


def handle_client(conn, addr):


    # getting username in same variable to save space
    username =  conn.recv(HEADER).decode(FORMAT)
    if username:
        username = int(username.strip())
        username = conn.recv(username).decode(FORMAT)
        if not username:
            username = addr


    clients.append(conn) 

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

                if not message:
                    continue

                # maintain messages sent 
                message_log = {"username" : username,
                                "message" : message,
                                "time" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                
                messages.append(message_log)
                message_queue.put((addr, message_log))
                
                if message == DISCONNECT_MESSAGE:
                    connected = False
                
                print(f"[{username}]: {message}")
                conn.recv(0)
        except ConnectionResetError as err:
            print(f"\n{username} severed the connection forcefully.")
            connected = False


    print(f"{username} disconnected.\n")
    print(f"{username} disconnected.\n")
    conn.close()



def start_server():
    server_socket.listen()
    print(f"[Listening] IP = {SERVER}, {PORT=}")

    broadcaster = threading.Thread(target=broardcast_new_messages, daemon=True)
    broadcaster.start()

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr)).start()
        print(f"[Active Threads] : {threading.active_count() - 1}")
        print(f"[Active Connections] : {int((threading.active_count() - 1)/2)}")

 

print("STARTING SERVER...")
start_server()