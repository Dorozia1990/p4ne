#imports
from pysnmp.hlapi import * # Импортировать только High-level API

#defs
snmp_object = ObjectIdentity('1.3.6.1.2.1.2.2.1.2')
snmp_ver = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
ipaddr_string = '10.31.70.107'
port_int = 161
varBindsIndex = 3

result = getCmd(
	SnmpEngine(),
	CommunityData('public', mpModel = 0),
	UdpTransportTarget((ipaddr_string, port_int)),
	ContextData(),
	ObjectType(snmp_ver)
)
#result: (errorIndication, errorStatus, errorIndex, varBinds)

result2 = nextCmd(
	SnmpEngine(),
	CommunityData('public', mpModel = 0),
	UdpTransportTarget((ipaddr_string, port_int)),
	ContextData(),
	ObjectType(snmp_object),
	lexicographicMode = False
)
#result2: (errorIndication, errorStatus, errorIndex, varBinds)

#executable

for i in result:
	for j in i[varBindsIndex]:
		print(j)

for i in result2:
	for j in i[varBindsIndex]:
		print(j)