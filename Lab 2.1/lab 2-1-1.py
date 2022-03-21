# imports
import paramiko, time, re


# initialization

BUF_SIZE = 20000
TIMEOUT = 1
L21_HOST = "10.31.70.209"
LOGIN = "restapi"
PASS = "j0sg1280-7@"
intList = []
inputPacketsList = []
inputBytesList = []
outputPacketsList = []
outputBytesList = []
finalDict = {}

ssh_connection = paramiko.SSHClient()
ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# executable

# receiving interfaces

ssh_connection.connect(L21_HOST, username=LOGIN, password=PASS, look_for_keys=False, allow_agent=False)
session = ssh_connection.invoke_shell()

session.send("terminal length 0\n")
time.sleep(TIMEOUT)
session.send("show interface\n")
time.sleep(TIMEOUT*2)
s = session.recv(BUF_SIZE).decode()
session.close()

# processing interfaces

s1 = s.split("\n")
for everyString in s1:
    if everyString.rfind("csr-api") == -1:
        matcherInt = re.match(".([a-zA-Z0-9])+", everyString)
        matcherInput = re.match("^( {5})((?:[0-9])+)( packets input, )((?:[0-9])+)( bytes, )((?:[0-9])+)( no buffer)",
                                everyString)
        matcherOutput = re.match("^( {5})((?:[0-9])+)( packets output, )((?:[0-9])+)( bytes, )((?:[0-9])+)( underruns)",
                                everyString)
        if bool(matcherInt):
            intList.append(matcherInt.group(0))
        if bool(matcherInput):
            inputPacketsList.append(matcherInput.group(2))
            inputBytesList.append(matcherInput.group(4))
        if bool(matcherOutput):
            outputPacketsList.append(matcherOutput.group(2))
            outputBytesList.append(matcherOutput.group(4))

# Forming output dictionary

for i in range(len(intList)):
    finalDict.update({intList[i]: {"inPa": inputPacketsList[i], "InBy": inputBytesList[i], "outPa": outputPacketsList[i], "outBy": outputBytesList[i]}})

print(finalDict)
