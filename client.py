import socket
import threading

def find_open_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MESSAGE = "!dsc"
PORT = 5050

SERVER = "192.168.1.4"  # IP you want to connect
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(message):
    message = message.encode(FORMAT)
    msg_len_str = str(len(message)).encode('utf-8')
    msg_len_str += b' ' * (HEADER - len(msg_len_str))
    client.send(msg_len_str)
    client.send(message)

connected = True

inp = input("Enter Username : ")
send(inp)

while connected:
    inp = input("[YOU] : ")
    send(inp)
    if inp == DISCONNECT_MESSAGE:
        connected = False

print("\n------------You have exitted the chat successfully------------\n")