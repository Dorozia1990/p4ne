# imports

from flask import Flask
import glob
from ipaddress import IPv4Interface
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
import re
import json
import ssl
import requests
import urllib3
import datetime

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

# defs

L22_HOST = "https://10.31.70.210:55443"
LOGIN = "restapi"
PASS = "j0sg1280-7@"
TIMEZONE_DIFF = 3
deathTime = datetime.datetime(1970, 1, 1, 0, 0, 0)
token = ""

# Klochkov class
class Ssl1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


# months transition

def takeMonth(strMonth):
    d = {"Jan ": 1,
         "Feb ": 2,
         "Mar ": 3,
         "Apr ": 4,
         "May ": 5,
         "Jun ": 6,
         "Jul ": 7,
         "Aug ": 8,
         "Sep ": 9,
         "Oct ": 10,
         "Nov ": 11,
         "Dec ": 12,
         }
    return d[strMonth]


#authorizeAndCheck
def authAndC(currentToken, deathTime):
    if (deathTime < datetime.datetime.now()) or (currentToken == ""):
        r = s.get(L22_HOST, verify=False)
        r = s.post(L22_HOST + '/api/v1/auth/token-services', auth=(LOGIN, PASS), verify=False)
        token = r.json()['token-id']
        #print(r.json()['expiry-time'])
        timeMatch = re.match("^(([a-zA-Z]{3} ){2})([0-9]*) ([0-9]*):([0-9]*):([0-9]*) ([0-9]{4})", r.json()['expiry-time'])
        hour = str(int(timeMatch.group(4)) + TIMEZONE_DIFF)
        deathTime = datetime.datetime.strptime(r.json()['expiry-time'], "%c")
    #    print(r.json())
    #    global tokenDeathTime = r.json()[]
    else:
        pass
    return token, deathTime

# startup

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
s = requests.Session()
s.mount(L22_HOST, Ssl1HttpAdapter())

token, deathTime = authAndC(token, deathTime)

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
    return "/configs - лист хостов <br>" \
           "/config/[hostname]/ - конфиг [hostname] <br>"\
           "/cisco/processes/ - список процессов на Cisco <br>"

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

@app.route("/cisco/processes/")
def proc():
    header = {"content-type": "application/json", "X-Auth-Token": token}
    x = s.get(L22_HOST + '/api/v1/global/memory/processes', headers=header, verify=False)
    return x.json()

if __name__ == '__main__':
    app.run(debug=True)
