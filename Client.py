import json,socket,os
from datetime import datetime

#Setting variables for connection
serverName = 'localhost'
serverPort = 17703
bufferSize = 65536

#Connection to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#Reception and decoding of the messages sent by the server
info = clientSocket.recv(bufferSize).decode()
clientSocket.send("TMB".encode())
infoJson = json.loads(info)

routingTable = clientSocket.recv(bufferSize).decode()
clientSocket.send("TMB".encode())
dns = clientSocket.recv(bufferSize).decode()
clientSocket.send("TMB".encode())


#Building the path of the direcotry to create based on OS and timestamp
if(infoJson['platformInfo']['platform'] == "Windows"):
    path = "Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-version'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
else:
    path = "Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-release'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")

#Creation of server's subdirectory if doesn't exist
if not os.path.isdir(path):
    try:
        os.makedirs(path)
        with open(path + "/SystemInformation.JSON", "w") as file:
            file.write(info)
            
        with open(path + "/RoutingTable.txt", "w") as file:
            file.write(routingTable)
            
        with open(path + "/DNS.txt", "w") as file:
            file.write(dns)
 
    except OSError:
        print ("Creation of the subdirectory \"{path}\" failed")
        
#Print of all the system information of the server
print(info)
print(routingTable)
print(dns)

#Obtaining files from the Server
fileName = clientSocket.recv(bufferSize).decode()
clientSocket.send("TMB".encode())
fileSize = clientSocket.recv(bufferSize).decode()
clientSocket.send("TMB".encode())

print("Received new File: " + fileName + "\t" + fileSize + "B")  

done = False

with open (path + "/" + fileName, "wb") as f:
	fileBytes = b""
	while not done:
		if fileBytes[-5:] == b"<TMB>":
			done = True
		else:
			data = clientSocket.recv(bufferSize)
			fileBytes += data
	f.write(fileBytes[:-5])
clientSocket.close()
