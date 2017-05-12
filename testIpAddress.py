#!/usr/bin/python3

import socket




# from https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


print('looking up IP address')
print(get_ip_address())






import ipaddress
import sys

for arg in sys.argv[1:]:
    addr = ipaddress.ip_interface(arg)
    print("address =", addr)
    print("network =", addr.network)
    if addr.version == 4:
        print("netmask =", addr.netmask)
        print("broadcast =", addr.network.broadcast_address)
    print()
    
    