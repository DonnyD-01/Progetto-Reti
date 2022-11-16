import json,socket,os

#Setting variables for connection
serverName = 'localhost'
serverPort = 17703

#Connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#Creating the file with the Information 
jsonfile = open("SystemInformation.JSON", 'w')

#Reception and decoding of the messages sent by the server
info = clientSocket.recv(4096)
jsonfile.write(info.decode())
print(info.decode())

#Closing file and connection
jsonfile.close()
clientSocket.close()
