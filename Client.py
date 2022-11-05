import json,socket

#Setting variables for connection
serverName = 'localhost'
serverPort = 12000

#Connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#Reception and decoding of the messages sent by the server
for x in range (8):
	modifiedSentence = clientSocket.recv(1024)
	print(modifiedSentence.decode())
clientSocket.close()
