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
TOP_Q = 10

def cheekySrt(srtDict):
    return srtDict["memory-used"]

# executable

s = requests.Session()
s.mount(L22_HOST, Ssl1HttpAdapter())

r = s.get(L22_HOST, verify=False)
r = s.post(L22_HOST + '/api/v1/auth/token-services', auth=(LOGIN, PASS), verify=False)
token = r.json()['token-id']
header = {"content-type": "application/json", "X-Auth-Token": token}
r = s.get(L22_HOST + '/api/v1/global/memory/processes', headers=header, verify=False)
processList = r.json()["processes"]


srtList = sorted(processList, key=cheekySrt, reverse=True)
print("Top", TOP_Q, "memory wasting processes:")
for eachList in range(TOP_Q):
    print(srtList[eachList]["process-name"])
