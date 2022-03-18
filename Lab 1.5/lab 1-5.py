#imports

import glob

#initialization


fileList = glob.glob("..\config_files\*.txt")
networkList = []
stringNeeded = " ip address "

#executable

for eachFile in fileList:
    with open(eachFile, "rt") as currentFile:
        eachLine = currentFile.readlines()
        for line in eachLine:
            if (stringNeeded in line) and (line.find("ip address") == 1):
                networkList.append(line.strip("\n"))

networkList = list(set(networkList))
for network in networkList:
    print(network)
