import socket
import threading

# connection data
host = '192.168.56.105' 
port = 8080

# connect socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#list of clients and their names
clients = []
names = []

#send message to all clients that connected
def broadcast(message):
	for client in clients:
		client.send(message)

#control message from clients
def control(client):
	while True:
		try: 
			#broadcast the message to all the clients connected
			message = client.recv(1024)
			broadcast(message)
		except:
			# close and remove client
			index = clients.index(client)
			clients.remove(client)
			client.close()
			name = names[index]
			broadcast(f'{name} left the chat!'.encode('ascii'))
			names.remove(name)
			break

#listen from client
def receive():
	while True:

		#accept connection
		client, address = server.accept()
		print(f"Connected with {str(address)}")
		
		#request name and stored
		client.send('NICK'.encode('ascii'))
		name = client.recv(1024).decode('ascii')
		names.append(name)
		clients.append(client)

		#print and broadcast name
		print(f'Client name is {name}!')
		broadcast(f'{name} is joining the chatroom!'.encode('ascii'))
		client.send('Connected to the server!'.encode('ascii'))

		#start controllong thread for client
		thread = threading.Thread(target=control, args=(client,))
		thread.start()

print("Server is listening...")
receive()
