import platform, re, uuid, socket, psutil, json, cpuinfo, datetime

#Getting information about the system
systemInfo = {}
try:	
	systemInfo['boot-time']=datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
	systemInfo['platform'] = platform.system()
	systemInfo['platform-release'] = platform.release()
	systemInfo['platform-version'] = platform.version()
	systemInfo['architecture'] = platform.machine()
	users = psutil.users() 
	i=1
	for user in users:
		systemInfo['user' +str(i) + "_name"] = user.name 
		systemInfo['user' +str(i) + "_host"] = user.host
		i += 1
except: 
	systemInfo['error'] = "Cannot Recover additional System Information"

#Getting information about the CPU
cpuInfo = {}
try:
	cpuInfo['cpu'] = cpuinfo.get_cpu_info()['brand_raw']
	cpuInfo['cores'] = psutil.cpu_count(logical = False)
	cpuInfo['threads'] = psutil.cpu_count()
	cpuInfo['total-usage'] = str(psutil.cpu_percent()) + "%"
	cpuFreq=psutil.cpu_freq()
	cpuInfo['max-frequency'] = str(round(cpuFreq.max, 2)) + "MHz"
	cpuInfo['current-frequency'] = str(round(cpuFreq.current, 2)) + "MHz" 
	cpuInfo['min-frequency'] = str(round(cpuFreq.min, 2)) + "MHz"
except:
	cpuInfo['error'] = "Cannot Recover additional CPU Information"

#Getting information about the Memory
memoryInfo = {}
try:
	ram=psutil.virtual_memory()
	memoryInfo['ram-size'] = str(round(ram.total / (1024.0 ** 3), 2)) + "GB"
	memoryInfo['available'] = str(round(ram.available / (1024.0 ** 3), 2)) + "GB"
	memoryInfo['used'] = str(round(ram.used / (1024.0 ** 3), 2)) + "GB"
	memoryInfo['percentage-used'] = str(ram.percent) +"%"
	memoryInfo['swap-memory'] = str(round(psutil.swap_memory().total / (1024.0 ** 3), 2)) + "GB"
except:
	memoryInfo['error'] = "Cannot Recover additional Memory Information"

#Getting information about the disks
diskInfo = {}
try:
	partitions = psutil.disk_partitions()
	i = 1
	for partition in partitions:
		diskInfo['disk' + str(i) + '-name'] = partition.device
		diskInfo['disk' + str(i) + '-mountpoint'] = partition.mountpoint
		diskInfo['disk' + str(i) + '-filesystem'] = partition.fstype
		partition_usage = psutil.disk_usage(partition.mountpoint)
		diskInfo['disk' + str(i) + '-totalsize'] = str(partition_usage.total // (1024 ** 3)) + "GB"
		diskInfo['disk' + str(i) + '-free'] = str(partition_usage.free // (1024 ** 3)) + "GB"
		i += 1
except:
	diskInfo['error'] = "Cannot recover additional Disks Information"

#Getting information about the network card
networkInfo = {}
try:
	networkInfo['hostname'] = socket.gethostname()
	networkInfo['ip-address'] = socket.gethostbyname(socket.gethostname())
	networkInfo['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
	net_io = psutil.net_io_counters()
	networkInfo['bytes-sent'] = str(round(net_io.bytes_sent / (1024 ** 2), 2)) + "MB"
	networkInfo['bytes-received'] = str(round(net_io.bytes_recv / (1024 ** 2), 2)) + "MB"
except:
	networkInfo['error'] = "Cannot recover additional Network Information"

#Getting information about the battery
batteryInfo = {}
try:
	battery = psutil.sensors_battery()
	batteryInfo['battery'] = "false"
	if battery != None :
		batteryInfo['battery'] = "true"
		batteryInfo['charge'] = str(battery.percent) + "%"
		batteryInfo['plugged'] = str(battery.power_plugged)
except:
	batteryInfo['error'] = "Cannot recover additional Battery Infomation"


#Network variables initialization for connection to the client 
serverPort = 17703
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

#Sending information obtained
while True:
	connectionSocket,addr = serverSocket.accept()
	connectionSocket.send(json.dumps(systemInfo, indent=4).encode())
	connectionSocket.send(json.dumps(cpuInfo, indent=4).encode())
	connectionSocket.send(json.dumps(memoryInfo, indent=4).encode())
	connectionSocket.send(json.dumps(diskInfo, indent=4).encode())
	connectionSocket.send(json.dumps(networkInfo, indent=4).encode())
	connectionSocket.send(json.dumps(batteryInfo, indent=4).encode())
	connectionSocket.close()
