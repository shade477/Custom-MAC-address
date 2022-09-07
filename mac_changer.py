import subprocess
import optparse
import re
from platform import system


def usr_data():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface", help="The interface name")
    parse_object.add_option("-m", "--mac_address", dest="mac_address", help="Custom MAC address")
    parse_object.add_option("-f","--find_interfaces", action="store_True",dest="find_interface",help="Detect all interfaces connected") 

    return parse_object.parse_args()


def mac_changer_proc(inter, mac_custom):
    if system() == 'Linux':
        subprocess.run(["ifconfig", inter, "down"])
        subprocess.run(["ifconfig", inter, "hw", "ether", mac_custom])
        subprocess.run(["ifconfig", inter, "up"])
    else:
        print("Not supported")


def display_proc(inter):
    if system() == 'Linux':
        ifconfig = subprocess.check_output(["ifconfig", inter])
        new_mac = re.search(br"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    if system() == 'Windows':
        ipconfig = subprocess.check_output(["ifconfig", inter])
        new_mac = re.search(br"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)
    
    if new_mac:
        return new_mac.group(0)
    else:
        return None

def dis_interface():
    if system() == 'Linux':
        print(subprocess.check_output("ifconfig -a", shell=True, universal_newlines=True))
    if system() == 'Windows':
        print(subprocess.check_output("ipconfig -all", shell=True, universal_newlines=True))

print("Mac-changer initiated")
(usr_input, args) = usr_data()
if usr_input.find_interface:
    dis_interface()
        
else:    
    mac_changer_proc(usr_input.interface, usr_input.mac_address)
    finalize = display_proc(usr_input.interface).decode()

    print("Result")
    if finalize == usr_input.mac_address:
        print(usr_input.interface + " address updated to " + usr_input.mac_address)
        #print("Success")
    else:
        print("Invalid Address Provided")