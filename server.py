#!/usr/bin/python

import threading, socket, signal, os, logging, sys
from datetime import date

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\u001b[3m'
    UNDERLINE = '\033[4m'

version = "1.0.2"

DEBUG = True

logging.basicConfig(level=logging.INFO, filename="info.log", filemode="w", format="%(levelname)s: %(asctime)s - %(message)s")

#host = "192.168.178.52"
#host = "192.168.2.118"
#host = "127.0.0.1"
#port = 2708
dummy_int = 123
dummy_str = "Hello World"
dummy_float = 1.23
dummy_array = [123, "hello", 1.23]

key = input("Please enter key:\n>>")

codec = 'ascii'

host = input("Please enter device IP or blank for: '127.0.0.1'\n>>")
if host == "":
    host = '127.0.0.1'
port = input("Please enter unused Port or blank for: '2708'\n>>")
if port == "":
    port = 2708
if type(port) == type(dummy_str):
    port = int(port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
logging.info(f"Initialized with address {host}:{port}")
clients = []
names = []
addresses = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			index = clients.index(client)
			name = names[index]
			logging.info(f"Received Message from {name}")
			if message.decode(codec) == ">Quit<":
				index = clients.index(client)
				clients.remove(client)
				client.close()
				name = names[index]
				addr = addresses[index]
				broadcast(f"{bcolors.OKCYAN}{name}{bcolors.ENDC} {bcolors.WARNING}left the server.{bcolors.ENDC}".encode(codec))
				logging.debug(f"{name} - {addr} disconnected")
				names.remove(name)
				addresses.remove(addr)
				break
			else:
				broadcast(message)
				logging.debug(f"Broadcasted Message from {name}")
		except:
			try:
				index = clients.index(client)
				clients.remove(client)
				client.close()
				name = names[index]
				addr = addresses[index]
				broadcast(f"{bcolors.OKCYAN}{name}{bcolors.ENDC} {bcolors.WARNING}left the server.{bcolors.ENDC}".encode(codec))
				logging.info(f"{name} - {addr} diconnected; caused by error!")
				names.remove(name)
				addresses.remove(addr)
			except:
				pass
			break
def shell():
    while True:   
        try:
            cmd = input("")
            match cmd:
                case "help":
                    print("Commands:\nhelp - show this help\nquit - stop server\nlscli - List Names of the connected Clients\nlsaddr - list connected clients with names and adresses\nkick - diconnect user, but can still reconnect\ninfo - list server info")

                case "lscli":
                    print(f"Connected Clients:\n{names}")
                    logging.info(f"lscli: Connected Clients:\n{names}")

                case "quit":
                    logging.info("Server Shutdown, reqested by user via Shell")
                    os.kill(os.getpid(), signal.SIGTERM)
                    break

                case "lsaddr":
                    print("Connected Clients:")
                    logging.info("lsaddr: Connected Clients:")
                    for ix in range(len(addresses)):
                        print(f"{bcolors.OKBLUE}{names[ix]}{bcolors.ENDC}: {addresses[ix]}")
                        logging.info(f"{names[ix]}: {addresses[ix]}")

                case "info":
                    print(f"server address: {host}\nserver port: {port}\nconnected users: {len(clients)}\nkey: {key}\nversion: {version}")

                case "kick":
                    try:
                        k_user = input("Name of the user to be kicked: \n>> ")
                        index = names.index(k_user)
                        client = clients[index]
                        client.send(">KICKED<".encode(codec))
                        clients.remove(client)
                        client.close()
                        name = names[index]
                        addr = addresses[index]
                        broadcast(f"{bcolors.OKCYAN}{name}{bcolors.ENDC} {bcolors.WARNING}got kicked from the server.{bcolors.ENDC}".encode(codec))
                        logging.info(f"{name} - {addr} got kicked")
                        names.remove(name)
                        addresses.remove(addr)
                        print(f"{bcolors.OKGREEN}Kicked successfully!{bcolors.ENDC}")
                    except:
                        print(f"{bcolors.WARNING}User not found!{bcolors.ENDC}") 

                case _:
                    print(f"{bcolors.WARNING}Command not found, please enter 'help' for help!{bcolors.ENDC}")

        except:
            print(f"{bcolors.FAIL}An error occured!{bcolors.ENDC}")   
                    

"""	
		try:
			cmd = input("")
			if cmd == "help":
				print("Commands:\nhelp - show this help\nquit - stop server\nlscli - List Names of the connected Clients\nlsaddr - list connected clients with names and adresses\nkick - diconnect user, but can still reconnect")
			elif cmd == "lscli":
				print(f"Connected Clients:\n{names}")
				logging.info(f"lscli: Connected Clients:\n{names}")
			elif cmd == "quit":
				logging.info("Server Shutdown, reqested by user via Shell")
				os.kill(os.getpid(), signal.SIGTERM)
				break
			elif cmd == "lsaddr":
				print("Connected Clients:")
				logging.info("lsaddr: Connected Clients:")
				for ix in range(len(addresses)):
					print(f"{bcolors.OKBLUE}{names[ix]}{bcolors.ENDC}: {addresses[ix]}")
					logging.info(f"{names[ix]}: {addresses[ix]}")
			elif cmd == "info":
			    print(f"")
			elif cmd == "kick":
				try:
					k_user = input("Name of the user to be kicked: \n>> ")
					index = names.index(k_user)
					client = clients[index]
					client.send(">KICKED<".encode(codec))
					clients.remove(client)
					client.close()
					name = names[index]
					addr = addresses[index]
					broadcast(f"{bcolors.OKCYAN}{name}{bcolors.ENDC} {bcolors.WARNING}got kicked from the server.{bcolors.ENDC}".encode(codec))
					logging.info(f"{name} - {addr} got kicked")
					names.remove(name)
					addresses.remove(addr)
					print(f"{bcolors.OKGREEN}Kicked successfully!{bcolors.ENDC}")
				except:
					print(f"{bcolors.WARNING}User not found!{bcolors.ENDC}")
			else:
				print(f"{bcolors.WARNING}Command not found, please enter 'help' for help!{bcolors.ENDC}")

		except:
			print(f"{bcolors.FAIL}An error occured!{bcolors.ENDC}")
"""
def receive():
	thread_shell = threading.Thread(target=shell, daemon=True)
	thread_shell.start()
	while True:
		client, addr = server.accept()
		client.send(">NAME<".encode(codec))
		name = client.recv(1024).decode(codec)
		client.send(">VERSION<".encode(codec))
		client_version = client.recv(1024).decode(codec)
		client.send(">KEY<".encode(codec))
		client_key = client.recv(1024).decode(codec)
		if client_version != version:
			client.send(">WRONG_VERSION<".encode(codec))
		elif client_key != key:
			client.send(">WRONG_KEY<".encode(codec))
		else:
			print(bcolors.OKCYAN + "New Connection: " + str(addr) + " " + name + bcolors.ENDC)
			names.append(name)
			addresses.append(addr)
			clients.append(client)
			client.send(f"{bcolors.OKGREEN}Connection successfull{bcolors.ENDC}".encode(codec))
			broadcast(f"{bcolors.OKCYAN}{name}{bcolors.ENDC} {bcolors.WARNING}joined the server.{bcolors.ENDC}".encode(codec))
			thread =  threading.Thread(target=handle, args=(client,), daemon=True)
			thread.start()


print(f"{bcolors.OKBLUE}Server is starting...{bcolors.ENDC}")

if DEBUG:
	receive()
else:
	try:
		receive()
	except:
		print(f"{bcolors.FAIL}Error: set DEBUG = true to see detailed error message!{bcolors.ENDC}")
