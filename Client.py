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
clientSocket.close()
infoJson = json.loads(info)

#Building the path of the direcotry to create based on OS and timestamp
if(infoJson['platformInfo']['platform'] == "Windows"):
    path = "Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-version'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
else:
    path = "Retrieved/" + infoJson['platformInfo']['platform'] + " " + infoJson['platformInfo']['platform-release'] + " " + datetime.now().strftime("%d-%m-%Y %H-%M-%S")

#Creation of server's subdirectory if doesn't exist
if not os.path.isdir(path):
    try:
        os.makedirs(path)
        jsonFile = open(path + "/SystemInformation.JSON", 'w')
        jsonFile.write(info)
        jsonFile.close()
    except OSError:
        print (f"Creation of the subdirectory \"{path}\" failed")

#Print of all the system information of the server
print(info)