import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "192.168.1.4"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("CONNECTED")

def dir():
	type_s = ("send").encode(FORMAT)
	client.send(type_s)

	message_s = ("cd").encode(FORMAT)
	msg_length_s = len(message_s)
	send_length_s = str(msg_length_s).encode(FORMAT)
	send_length_s += b' ' * (HEADER - len(send_length_s))
	client.send(send_length_s)
	client.send(message_s)

	global dirr
	
	dirr = client.recv(1048576).decode(FORMAT)
def disconnect():
	message = ("!disconnect").encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	
def send(msg, msg_type):
	if msg_type == "file":
		type_ = msg_type.encode(FORMAT)
		client.send(type_)
		
		message = msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (HEADER - len(send_length))
		client.send(send_length)
		client.send(message)
	if msg_type == "send":
		type_s = msg_type.encode(FORMAT)
		client.send(type_s)

		message_s = msg.encode(FORMAT)
		msg_length_s = len(message_s)
		send_length_s = str(msg_length_s).encode(FORMAT)
		send_length_s += b' ' * (HEADER - len(send_length_s))
		client.send(send_length_s)
		client.send(message_s)


def file_recive():
	data = client.recv(1048576).decode(FORMAT)
	item = data.split("_")
	FILENAME = item[0]
	FILESIZE = int(item[1])

	with open(f"recv_{FILENAME}", "wb") as f:
		data = client.recv(1048576)
		f.write(data)

def recive():
	output = client.recv(1048576).decode(FORMAT)
	print(output)
	

check = input("Would like to run commands(C) or operations(O): ")

if check == "O":
	while True:
		msg_type = input("Enter Type: ")
		command = input("Command: ")
		if command  == "quit":
			disconnect()
			print("[DISCONNECTED]...")
			break
		if msg_type == "file":
			send(command, msg_type)
			file_recive()
		elif msg_type == "send":
			send(command, msg_type)
			recive()
if check == "C":
	while True:
		o_p = input(f"{dirr}>")
		if o_p == "quit":
			disconnect()
			print("[DISCONNECTED]")
			break
		else:
			send(o_p, "send")
			recive()
