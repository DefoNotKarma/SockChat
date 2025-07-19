import socket
import threading
import bz2
import json
from queue import Queue
import sys

FORMAT = 'utf-8'
HEADER = 8       # bytes
LOG_HEADER = 64
HEADER = 8       # bytes
LOG_HEADER = 64
DISCONNECT_MESSAGE = "!dsc"
PORT = int(input("Enter Port Number : ")) 

SERVER = str(input("Enter IP : "))
ADDR = (SERVER, PORT)
BLANK_HEADER = str(len("")).encode(FORMAT)
BLANK_HEADER += b' ' * (HEADER - len(BLANK_HEADER))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

user_input_queue = Queue()

def get_user_input():
    while True:
        user_input = input()
        user_input_queue.put(user_input)
        print("\033[F", end='') # return to prev line
        #sys.stdout.flush()


def recieve_messages():
    while True:
        message_size = client.recv(HEADER)
        if message_size:
            message_size = int(message_size.strip())
            message = json.loads(client.recv(message_size).decode(FORMAT))

            print(f"\r[{message['time']}] [{message['username']}] : {message["message"]}")

            

def send(message):
    message = message.encode(FORMAT)
    msg_len_str = str(len(message)).encode(FORMAT)
    msg_len_str = str(len(message)).encode(FORMAT)
    msg_len_str += b' ' * (HEADER - len(msg_len_str))
    client.send(msg_len_str)
    client.send(message)
    blank_header = str(0).encode(FORMAT).ljust(HEADER)
    client.send(blank_header)  

def handle_send_messages():
    global connected
    while connected:
        if not user_input_queue.empty():
            inp = user_input_queue.get()
            if inp.strip():
                send(inp)
                print(f"[YOU] : {inp}")
                sys.stdout.flush()
            if inp == DISCONNECT_MESSAGE:
                connected = False

connected = True

inp = input("Enter Username : ")
send(inp)

print(f"fetching logs...\n")

logs_size = client.recv(LOG_HEADER)
if logs_size:

    logs_size = int(logs_size.strip())
    logs = client.recv(logs_size)
    logs = json.loads(bz2.decompress(logs))

    if logs == []:
        print("No logs to display.")
    else:

        for msg in logs:
            print(f"[{msg['time']}] [{msg['username']}] : {msg['message']}")

else:
    print("couldn't fetch logs.")

print("\n")

get_input = threading.Thread(target=get_user_input, daemon=True).start()
listener = threading.Thread(target=handle_send_messages, daemon=True)
listener.start()

try:

    recieve_messages()

except KeyboardInterrupt:
    print("\nDisconnecting...")
    connected = False
    send(DISCONNECT_MESSAGE)

finally:
    print("\n------------You have exitted the chat------------\n")

