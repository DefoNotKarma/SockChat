import socket
import threading
import bz2
import json

def find_open_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

FORMAT = 'utf-8'
HEADER = 8       # bytes
LOG_HEADER = 64
DISCONNECT_MESSAGE = "!dsc"
PORT = 5050

SERVER = "192.168.1.4"  # IP you want to connect
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recieve_messages():
    message_size = client.recv(HEADER)
    if message_size:
        message_size = int(message_size.strip())
        message = client.recv(message_size)
        print(f"[{message['username']}] : {message["message"]}")


def send(message):
    message = message.encode(FORMAT)
    msg_len_str = str(len(message)).encode(FORMAT)
    msg_len_str += b' ' * (HEADER - len(msg_len_str))
    client.send(msg_len_str)
    client.send(message)

connected = True

inp = input("Enter Username : ")
send(inp)

print(f"fetching logs...\n")

logs_size = client.recv(LOG_HEADER)
if logs_size:
    print(f"fetching logs...\n")
    logs_size = int(logs_size.strip())
    logs = client.recv(logs_size)
    decompressed = json.loads(bz2.decompress(logs))
    for msg in decompressed:
        print(f"[{msg['time']}] [{msg['username']}] : {msg['message']}")

elif logs_size == 0:
    print("No logs to display")

else:
    print("couldn't fetch logs.")

print("\n\n")

listener = threading.Thread(target=recieve_messages, daemon=True)
listener.start()



while connected:
    inp = input("[YOU] : ")
    send(inp)
    if inp == DISCONNECT_MESSAGE:
        connected = False

print("\n------------You have exitted the chat successfully------------\n")