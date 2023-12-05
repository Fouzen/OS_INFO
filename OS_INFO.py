#!/usr/bin/python3

# import python modules
import os
import platform
import socket
from requests import get
import subprocess
import psutil
import operator
import time

# Get OS Version
def display_os_version():
	# Get OS name, release and version
	os_name = platform.system()
	os_release = platform.release()
	os_version = platform.version()
	print('OS: \t\t', os_name)
	print('Release: \t', os_release)
	print('OS version: \t', os_version)

# Get private IP address
def get_private_ipaddr():
	# Create a socket and connect to google DNS at port 80 using UDP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	
	# Get the private IP Address
	private_ip = s.getsockname()[0]
	print("\nPrivate IP address: ", private_ip)
	
	# Close socket
	s.close()

# Get public IP address
def get_public_ipaddr():
	# Use ipify API to get public IP Address 
	ip = get('https://api.ipify.org').text
	print('Public IP address: {}'.format(ip))

# Get default IP address of gateway
def get_default_gateway():
	gateway = subprocess.check_output(["ip", "route"]).decode("utf-8")
	for line in gateway.split("\n"):
		if "default" in line:
			parts = line.split()
			gateway = parts[2]
			break
			
	print('Gateway IP address', gateway)

# Get hard disk info for total disk size, free space and used space
def get_hard_disk_size_info():
	disk_usage = psutil.disk_usage('/')

	# Get total disk size
	total_space = disk_usage.total / (1024**3)
	# Get free disk space
	free_space = disk_usage.free / (1024**3)
	# Get used disk space
	used_space = disk_usage.used / (1024**3)
	
	print("\nTotal Disk Space: {:.2f} GB".format(total_space))
	print("Free Disk Space: {:.2f} GB".format(free_space))
	print("Used Disk Space: {:.2f} GB".format(used_space))

# Get all directory sizes
def get_directory_sizes(path):
    directory_sizes = {}
    
    for dirpath, dirnames, filenames in os.walk(path):
        total_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for filename in filenames)
        directory_sizes[dirpath] = total_size
    
    return directory_sizes
    
# Sort top directories from largest to smallest 
def display_top_directories(directory_sizes, num_directories=5):
    sorted_dirs = sorted(directory_sizes.items(), key=operator.itemgetter(1), reverse=True)
    
    print("\nTop {} Directories:".format(num_directories))
    for i, (dirpath, size) in enumerate(sorted_dirs[:num_directories], 1):
        print("{}. {} - {:.2f} MB".format(i, dirpath, size / (1024**2)))

# Display and refresh CPU every 10 seconds
def display_cpu_usage():
	print()
	try:
		while True:
			cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
			print("CPU Usage: {:.2f}%".format(cpu_usage))
			time.sleep(10)
	except KeyboardInterrupt:
		print('interrupted!')

# Call function to display OS version
display_os_version()

# Display private address of local computer
get_private_ipaddr()

# Display public address of local network
get_public_ipaddr()

# Display gateway address of router
get_default_gateway()

# Display Hard disk size information
get_hard_disk_size_info()

# Path to scan in Kali linux Documents directory
path_to_scan = '/home/kali/Documents'

# Get the directory sizes
directory_sizes = get_directory_sizes(path_to_scan)	

# Display the top five directories
display_top_directories(directory_sizes, num_directories=5)

# Display current CPU usage in percentage
display_cpu_usage()
