import platform, re, uuid, socket, psutil, json, cpuinfo, datetime, sys

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
	systemInfo['memoryInfo']['percentage-used'] = str(ram.percent) +"%"
	systemInfo['memoryInfo']['swap-memory'] = str(round(psutil.swap_memory().total / (1024.0 ** 3), 2)) + "GB"
except:
	systemInfo['memoryInfo']['error'] = "Cannot Recover additional Memory Information"

#Getting information about the disks
systemInfo['diskInfo'] = {}
try:
	partitions = psutil.disk_partitions()
	i = 1
	for partition in partitions:
		systemInfo['diskInfo']['disk' + str(i) + '-name'] = partition.device
		systemInfo['diskInfo']['disk' + str(i) + '-mountpoint'] = partition.mountpoint
		systemInfo['diskInfo']['disk' + str(i) + '-filesystem'] = partition.fstype
		partition_usage = psutil.disk_usage(partition.mountpoint)
		systemInfo['diskInfo']['disk' + str(i) + '-totalsize'] = str(partition_usage.total // (1024 ** 3)) + "GB"
		systemInfo['diskInfo']['disk' + str(i) + '-free'] = str(partition_usage.free // (1024 ** 3)) + "GB"
		i += 1
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
	if battery != None :
		systemInfo['batteryInfo']['battery'] = "true"
		systemInfo['batteryInfo']['charge'] = str(battery.percent) + "%"
		systemInfo['batteryInfo']['plugged'] = str(battery.power_plugged)
except:
	systemInfo['batteryInfo']['error'] = "Cannot recover additional Battery Infomation"
	

#Network variables initialization for connection to the client 
serverPort = 17703
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

#Sending information obtained
while True:
	connectionSocket,addr = serverSocket.accept()
	connectionSocket.send(json.dumps(systemInfo,indent = 4).encode())
	connectionSocket.close()
