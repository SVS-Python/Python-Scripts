#!/usr/bin/python

import getopt,sys,paramiko,getpass,subprocess,os,datetime,time,re

# ensuring variales eist

commandfile, username, devicefile, password = "default", "default", "default", "default"

def usage():
    print "\nOptions: \n-h: help \n-l: device list \n-u: username \n-c: command list \n-p: password\n\nUsage: memLeakv1.py -u bob -l device-list.txt -c command-list.txt -p password\n"
    return

#This will error if unsupported parameters are received.
try:
    #this grabs input parameters. If the parameter requires an argument, it should have a colon ':' after. IE, -h does not require argument, -l, -u, -c do, so they get colons
    opts, args = getopt.getopt(sys.argv[1:], "hl:u:c:d:p:")
except getopt.GetoptError, err:
    #print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

#this loops through the given parameters and sets the variables. The letters o and a are arbitrary, antyhing can be used.
# this logic is 'if paramter = x, set variable'.

for o, a in opts:
    if o == "-l":
        devicefile = a
    elif o in ("-h"):
        usage()
        sys.exit()
    elif o in ("-u"):
        username = a
    elif o in ("-c"):
        commandfile = a
    elif o in ("-p"):
        password = a
    else:
        assert False, "unhandled option"

#this prints the given arguments
print "Username: ", username
print "Device List: ", devicefile
print "Command List: ", commandfile
print "passwordFromCLI: ", password


#password = getpass.getpass("What is your password? ")

#print "password: ", password

# Opens files in read mode
f1 = open(devicefile, "r")
f2 = open(commandfile, "r")

# Creates list based on f1 and f2
devices = f1.readlines()
commands = f2.readlines()

commands = "term len 0"

# this function loops through devices. No real need for a function here, just doing it.

def getPlatform(x):
    for device in x:
        #this scripts \n from end of each device (line) in the devices list
        device = device.rstrip()
        print "Device: ", device
        
        # this opens an SSH session and loops for every command in the file
#        for command in commands:
            #this strips \n from end of each command (line) in the commands list
        command = commands.rstrip()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # for debugging ONLY
        # paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
        #ssh.connect(device, username=username, password=password)
        ssh.connect(device, username=username, password=password, allow_agent=False, look_for_keys=False)
        ltime = time.strftime("%b_%d_%Y_%H_%M_%S", time.gmtime())
        
#        stdin, stdout, stderr = ssh.exec_command(command)
        command = "show run"
        stdin, stdout, stderr = ssh.exec_command(command)
        data = stdout.read()            
        print data
        outputTmp = ""
        outputTmp = data


        output = open(device + ltime + ".config", "a")
        output.write("\n============================================================\n")
        output.write("\n\nCommand Issued: "+command+ "at Time: " + ltime+"\n")
        output.writelines(outputTmp)
        output.write("\n============================================================\n")
        print "Your file has been updated, it is ", device+".out"
        
        ssh.close()
        
activeRP = getPlatform(devices)
f1.close()
f2.close()
