# imports

from flask import Flask
import glob
from ipaddress import IPv4Interface
import re

# init

fileList = glob.glob("..\config_files\*.txt")
ipList = []
intList = []
hostList = []
finalDict = {}

# internal definitions

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


# startup

for eachFile in fileList:
    with open(eachFile, "rt") as currentFile:
        eachLine = currentFile.readlines()
        for line in eachLine:
            lineDict = cheekyLine(line)
            if "ip" in lineDict:
                ipList.append(lineDict.get("ip"))
            if "int" in lineDict:
                intList.append(lineDict.get("int"))
            if "host" in lineDict:
                hostList.append(lineDict.get("host"))

        hostList = list(set(hostList))
        intList = list(set(intList))
        ipList = list(set(ipList))
        finalDict.update({hostList[0]: {"intList": intList, "ipList": ipList, }})
        ipList = []
        intList = []
        hostList = []

# web server definition
app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
    return "Никаких мануалов, только хардкор"

@app.route('/configs')
def page1():
    s = str(list(finalDict.keys()))
    return s

@app.route("/config/<hostname>/")
def page2(hostname):
    s = list(finalDict[hostname]['ipList'])
    x = []
    for everyIp in range(len(s)):
        x.append(str(s[everyIp]))
    x = str(x)
    return x

if __name__ == '__main__':
    app.run(debug=True)
