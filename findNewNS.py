import json
from collections import defaultdict

IDs = []
allParkedDomains = defaultdict(list)
newNS = defaultdict(list)
NSwithSepcialWords = {}
uniqueDomains = {}
errorStr = '\"http\":{}},\"error\":'

def parseZgrabJson(line):
    if line.find(errorStr) != -1:
        return
    hostNameStart = line.find('domain') + 9
    hostNameEnd = line.find('\"', hostNameStart)
    hostName = line[hostNameStart:hostNameEnd]
    for ID in IDs:
        if line.find(ID) != -1:
            allParkedDomains[ID].append(hostName)


def parseRR(line):
    data = json.loads(line)
    try:
        hostName = data['name']
        if hostName not in allParkedDomains or data['status'] == 'NO_ANSWER':
            return
        ts = []
        if len(data['data']['trace']) > 3:
            ts.append (data['data']['trace'][-2])
        if len(data['data']['trace']) > 0:
            ts.append (data['data']['trace'][-1])
        tmp = {}
        for t in ts:
            for auth in t['results']['authorities']:
                if auth['name'] != hostName:
                    tmp[auth['name']] = True
                if auth['answer'] != hostName:
                    tmp[auth['answer']] = True
        for dm in tmp.keys():
            if dm not in NSwithSepcialWords:
                newNS[dm].append(hostName)
                uniqueDomains[hostName] = True
    except:
        return

def writeResult(fName, d):
    with open(fName, 'w') as f:
        f.write('New Domains Count:' + str(len(uniqueDomains)) + '\n')
        f.write('New NS Count:' + str(len(d)) + '\n')
        for k,v in d:
            f.write(k + ':')
            for idx in range(len(v)-1):
                f.write(v[idx] + ',')
            f.write(v[-1] + '\n')

#read IDs
with open('fullID.txt') as f:
    lines = f.readlines()
IDs = [line.rstrip() for line in lines]


# find all domains found by ID
with open('/data1/nsrg/kwang40/fullData/2019-03-03/banners.json') as f:
    for line in f:
        if len(line) > 6:
            parseZgrabJson(line)
for k,v in allParkedDomains.items():
    allParkedDomains[k] = list(set(v))
print ('Finish Reading domains.')

# find all NS with special words
with open ('NSwithSepcialWords.txt') as f:
    for line in f:
        NSwithSepcialWords[line.rstrip()] = True

# find new NS by domains
with open ('/data1/nsrg/kwang40/fullData/2019-03-03/RR.json') as f:
    for line in f:
        parseRR(line)
for k,v in newNS.items():
    newNS[k] = list(set(v))
print ('Finish Reading NS.')

sorted_NS = sorted(newNS.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('newNSbyID.txt', sorted_NS)
with open('AllDomainCountByID', 'w') as f:
    for k,v in allParkedDomains:
        f.write(k+',' + str(len(v)) + '\n')
