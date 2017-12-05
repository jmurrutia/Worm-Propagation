# Worm Propagation

Team Members:   
	- Jose Urrutia (jmurrutia@csu.fullerton.edu)  

Attacker VM:  
	- jmurrutia-Lubuntu_1  

How to execute program:  
	- The worms must be launched from the attacker VM (jmurrutia-Lubuntu_1)  
	- Once in the attacker VM, change directory to /tmp  
		- This is where the 3 worms are located  
		
	- To launch the worm:  
		- Enter command "python <worm_name.py> attack"  
  
			- python: the python interpreter
  
			- worm_name.py: the name of the worm  
				- There are 3 worms to choose from:  
					- replicator_worm.py  
					- ransomware_worm.py  
					- backdoor_worm.py  
  
			- attack: a REQUIRED third argument that must be provided  
				- This allows the worm to differentiate between  
				  the attacker and a victim  
				- PREVENTS an attack on original attacker  
				- Any argument may be provided (i.e. "test", "OSS")  
  
Extra Credit:  
	- No extra credit attempt  
  
Special Notes:  
	- Each host victim (jmurrutia-Lubuntu_2 and jmurrutia-Lubuntu_3) contains a script, relevant to each worm, that will clean up the /tmp/ and /home/cpsc/ directories  
	- You may choose to use these scripts or not  
	- Execute the scripts from directory /root/Desktop  

	- ************************************************************  
	  When running backdoor_worm.py, be sure to replaced the  
	  hardcoded IP address of the attacker.  Endian has changed my  
	  attackers IP a few times now.  
	  ************************************************************  
	
