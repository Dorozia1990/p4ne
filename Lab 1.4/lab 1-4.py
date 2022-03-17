#imports

from ipaddress import IPv4Network
import random

#defs

class IPv4RandomNetwork(IPv4Network):
    def __init__(self):
        self.network_address = random.randint(0x0B000000, 0xDF000000)
        self.netmask = random.randint(8, 24)
        IPv4Network.__init__(self, (self.network_address, self.netmask), strict = 0)
    def key_value(self):
        return int(self.network_address)+int(self.netmask)*2**32

#executable

def keyFunc(addr):
    return addr.key_value()

n = IPv4RandomNetwork()
ipList = []
i = 0
while i < 50:
    tempNetwork = IPv4RandomNetwork()
    if not tempNetwork.is_private:
        ipList.append(tempNetwork)
        i += 1

newIpNetList = sorted(ipList, key = keyFunc)

for ipNet in newIpNetList:
    print(ipNet)