from os import get_terminal_size
import platform, re, uuid, socket, psutil, GPUtil, json, cpuinfo


#Getting information about the system
try:
	systemInfo = {}
	systemInfo['platform'] = platform.system()
	systemInfo['platform-release'] = platform.release()
	systemInfo['platform-version'] = platform.version()
	systemInfo['architecture'] = platform.machine()
except: 
	systemInfo['error'] = "Cannot Recover System Information"

#Getting information about the hardware
try:
	hardwareInfo = {}
	hardwareInfo['cpu'] = cpuinfo.get_cpu_info()['brand_raw']
	hardwareInfo['cores'] = psutil.cpu_count(logical = False)
	hardwareInfo['threads'] = psutil.cpu_count()
	hardwareInfo['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
	gpus = GPUtil.getGPUs()
	i = 1
	for gpu in gpus:
		hardwareInfo['gpu' + str(i) + '_name'] = gpu.name
		hardwareInfo['gpu' + str(i) + '_uuid'] = gpu.uuid
		hardwareInfo['gpu' + str(i) + '_vram'] = str(int(gpu.memoryTotal) // 1024) + " GB"
		i += 1
except:
	hardwareInfo['error'] = "Cannot recover Hardware Information"

#Getting information about the disks
try:
	diskInfo = {}
	partitions = psutil.disk_partitions()
	i = 1
	for partition in partitions:
		diskInfo['disk' + str(i) + '_name'] = partition.device
		diskInfo['disk' + str(i) + '_mountpoint'] = partition.mountpoint
		diskInfo['disk' + str(i) + '_filesystem'] = partition.fstype
		partition_usage = psutil.disk_usage(partition.mountpoint)
		diskInfo['disk' + str(i) + '_totalsize'] = str(partition_usage.total // (1024 ** 3)) + " GB"
		diskInfo['disk' + str(i) + '_free'] = str(partition_usage.free // (1024 ** 3)) + " GB"
		i += 1
except:
	diskInfo['error'] = "Cannot recover Disks Information"

#Getting information about the network card
try:
	networkInfo = {}
	networkInfo['hostname'] = socket.gethostname()
	networkInfo['ip-address'] = socket.gethostbyname(socket.gethostname())
	networkInfo['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
except:
	networkInfo['error'] = "Cannot recover Network Information"


#Network variables initialization for connection to the client 
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

#Sending information obtained
while True:
	connectionSocket,addr = serverSocket.accept()
	connectionSocket.send(json.dumps(systemInfo, indent=4).encode())
	connectionSocket.send(json.dumps(hardwareInfo, indent=4).encode())
	connectionSocket.send(json.dumps(diskInfo, indent=4).encode())
	connectionSocket.send(json.dumps(networkInfo, indent=4).encode())
	connectionSocket.close()