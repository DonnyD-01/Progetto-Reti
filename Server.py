import platform,re,uuid,socket,psutil,json
systemInfo={}
try:
	systemInfo['platform']=platform.system()
	systemInfo['platform-release']=platform.release()
	systemInfo['platform-version']=platform.version()
	systemInfo['architecture']=platform.machine()
except: 
	systemInfo['Error']="Cannot Recover System Information"
	
try:
	netWorkInfo={}
	netWorkInfo['hostname']=socket.gethostname()
	netWorkInfo['ip-address']=socket.gethostbyname(socket.gethostname())
	netWorkInfo['MAC-address']=':'.join(re.findall('..','%012x' % uuid.getnode()))
except:
	netWorkInfo['Error']="Cannot recover Network Information"
	
#try:

#except:
	#print("Cannot recover Boot Information")
	systemInfo['processor']=platform.processor()
	systemInfo['Ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"

serverPort=12000
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
while True:
    connectionSocket,addr=serverSocket.accept()
    connectionSocket.send(json.dumps(systemInfo, indent=4).encode())
    connectionSocket.send(json.dumps(netWorkInfo, indent=4).encode())
    connectionSocket.close()