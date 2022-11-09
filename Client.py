import json,socket,os

#Setting variables for connection
serverName = 'localhost'
serverPort = 17703

#Connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#If file exists, delete it
filepath = "SystemInformation.JSON"
if os.path.isfile(filepath):
	os.remove(filepath)
jsonfile = open(filepath, 'a')

#Reception and decoding of the messages sent by the server
for x in range (8):
	modifiedSentence = clientSocket.recv(1024)
	jsonfile.write(modifiedSentence.decode())
	print(modifiedSentence.decode())
jsonfile.close()
clientSocket.close()
