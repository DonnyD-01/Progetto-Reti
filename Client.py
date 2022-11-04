import json,socket
serverName= 'localhost'
serverPort=12000
clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
for x in range (2):
	modifiedSentence=clientSocket.recv(1024)
	print(modifiedSentence.decode())
clientSocket.close()