#!/usr/bin/python

import socket, threading, signal, os
import base64

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

version = "1.0.2"

name = input(f"{bcolors.BOLD}Please enter name:{bcolors.ENDC}\n>> ")

#host = "192.168.178.52"
#host = "192.168.2.118"
#host = "127.0.0.1"
#port = 2708

host = input("Please enter Server IP:\n>>")
port = int(input("Please enter Server Port:\n>>"))

key = input("Enter Key:\n>> ")

codec = 'ascii'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
    

def receive():
    while True:
        try:
            message = client.recv(1024).decode(codec)
            match message:
                case ">NAME<":
                    client.send(name.encode(codec))

                case ">VERSION<":
                    client.send(version.encode(codec))

                case ">KEY<":
                    client.send(key.encode(codec))

                case ">WRONG_VERSION<":
                    print(f"{bcolors.FAIL}Wrong version, please upgrade/downgrade!{bcolors.ENDC}")
                    os.kill(os.getpid(), signal.SIGTERM)

                case ">WRONG_KEY<":
                    print(f"{bcolors.WARNING}Wrong Key!{bcolors.ENDC}")
                    os.kill(os.getpid(), signal.SIGTERM)  

                case ">KICKED<":
                    print(f"{bcolors.WARNING}You got kicked!{bcolors.ENDC}")
                    os.kill(os.getpid(), signal.SIGTERM)

                case _:
                    print(message)

        except:
            print(f"{bcolors.FAIL}An error occured!{bcolors.ENDC}")
            client.close()
            os.kill(os.getpid(), signal.SIGTERM)
            break

'''
	    #try:
		message = client.recv(1024).decode(codec)
		if message == ">NAME<":
			client.send(name.encode(codec))
		elif message == ">VERSION<":
			client.send(version.encode(codec))
		elif message == ">KEY<":
			client.send(key.encode(codec))
		elif message == ">WRONG_VERSION<":
			print(f"{bcolors.FAIL}Wrong version, please upgrade/downgrade!{bcolors.ENDC}")
			os.kill(os.getpid(), signal.SIGTERM)
		elif message == ">WRONG_KEY<":
			print(f"{bcolors.WARNING}Wrong Key!{bcolors.ENDC}")
			os.kill(os.getpid(), signal.SIGTERM)
		elif message == ">KICKED<":
			print(f"{bcolors.WARNING}You got kicked!{bcolors.ENDC}")
			os.kill(os.getpid(), signal.SIGTERM)
		else:
			print(message)
	#except:
	#	print(f"{bcolors.FAIL}An error occured!{bcolors.ENDC}")
	#	client.close()
	#	os.kill(os.getpid(), signal.SIGTERM)
	#	break
'''

def write():
	while True:
		raw_msg = input("")
		if raw_msg == "%q":
			client.send(">Quit<".encode(codec))
			os.kill(os.getpid(), signal.SIGTERM)
			break
		else:
			message = f'{bcolors.OKCYAN}{name}:{bcolors.ENDC} {raw_msg}'
			client.send(message.encode(codec))

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()
