import socket
import threading

#client entering name
name = input("Enter your name:")

#connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.105', 8080))

#listen and sending name
def receive():
	while True:
		try:	#receive msg from server
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(name.encode('ascii'))
			else:
				print(message)

		except: #close connection when error
			print("Something goes wrong! error occurred!")
			client.close()
			break

#send msg to server
def typing():
	while True:
		message = f'{name}: {input("")}'
		client.send(message.encode('ascii'))

#starting threads for listening and typing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=typing)
write_thread.start()

