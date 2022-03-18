# imports

import glob
from ipaddress import IPv4Interface
import re


# initialization

fileList = glob.glob("..\config_files\*.txt")
ipList = []
intList = []
hostList = []

# definition
def cheekyLine(st):
        matcher = re.match("^( ip address) ((?:[0-9]{1,3}\.?){4}) ((?:[0-9]{1,3}\.?){4})$", st)
        if bool(matcher):
            return {"ip": (IPv4Interface(matcher.group(2) + "/" + matcher.group(3)))}
        else:
            matcher = re.match("(^(interface) ([0-9a-zA-Z ]*))", st)
            if bool(matcher):
                return {"int": matcher.group(3)}
            else:
                matcher = re.match("(^(hostname) ([0-9a-zA-Z ]*))", st)
                if bool(matcher):
                    return {"host": matcher.group(3)}
                else:
                    return {}

# executable

for eachFile in fileList:
    with open(eachFile, "rt") as currentFile:
        eachLine = currentFile.readlines()
        for line in eachLine:
            lineDict = cheekyLine(line)
            ipList.append(lineDict.get("ip"))
            intList.append(lineDict.get("int"))
            hostList.append(lineDict.get("host"))

ipList = list(set(ipList))
intList = list(set(intList))
hostList = list(set(hostList))

print("Список ip адресов:")
for ip in ipList:
    print(ip)
print("")

print("Список интерфейсов:")
for int in intList:
    print(int)
print("")

print("Список хостов")
for host in hostList:
    print(host)
