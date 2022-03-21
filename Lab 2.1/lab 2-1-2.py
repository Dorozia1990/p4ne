# imports
import json
import ssl
import requests
import urllib3
import pprint

from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

# defs
class Ssl1HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block, ssl_version=ssl.PROTOCOL_TLSv1)

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

L22_HOST = "https://10.31.70.210:55443"
LOGIN = "restapi"
PASS = "j0sg1280-7@"
ifNameList = []
inPa = []
outPa = []
finalDict = {}

# executable

s = requests.Session()
s.mount(L22_HOST, Ssl1HttpAdapter())

r = s.get(L22_HOST, verify=False)
r = s.post(L22_HOST + '/api/v1/auth/token-services', auth=(LOGIN, PASS), verify=False)
token = r.json()['token-id']
header = {"content-type": "application/json", "X-Auth-Token": token}
r = s.get(L22_HOST + '/api/v1/interfaces', headers=header, verify=False)
x = r.json()
for every in range(len(x["items"])):
    ifNameList.append(x["items"][every]["if-name"])

for everyInt in range(len(ifNameList)):
    r = s.get(L22_HOST + '/api/v1/interfaces/' + ifNameList[everyInt] + "/statistics", headers=header, verify=False)
    x = r.json()
    inPa.append(x["in-total-packets"])
    outPa.append(x["out-total-packets"])

print(ifNameList)
print(inPa)
print(outPa)

for i in range(len(ifNameList)):
    finalDict.update({ifNameList[i]: {"inPa": inPa[i], "outPa": outPa[i], }})

print(finalDict)
