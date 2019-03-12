import json
from collections import defaultdict

domainsByNS = {}
uniqueDomains = {}
newDomains = defaultdict(list)
def compareStrNoContain(s1, s2):
    return s2.find(s1) == -1

def parseRR(line):
    data = json.loads(line)
    try:
        hostName = data['name']
        if hostName not in uniqueDomains or data['status'] == 'NO_ANSWER':
            return
        ts = []
        if len(data['trace']) > 3:
            ts.append (data['trace'][-2])
        if len(data['trace']) > 0:
            ts.append (data['trace'][-1])
        tmp = {}
        for t in ts:
            for auth in t['results']['authorities']:
                if compareStrNoContain(auth['name'], hostName):
                    tmp[auth['name']] = True
                if compareStrNoContain(auth['answer'], hostName):
                    tmp[auth['answer']] = True
        for dm in tmp.keys():
            if dm in domainsByNS:
                if hostName not in domainsByNS[dm]:
                    newDomains[dm].append(hostName)
                uniqueDomains[hostName] = True
    except:
        return

def writeResult(fName, d):
    with open(fName, 'w') as f:
        f.write('All Domains Count:' + str(len(uniqueDomains)) + '\n')
        for k,v in d:
            f.write(k + ':')
            for idx in range(len(v)):
                f.write(v[idx] + ',')
            f.write('\n')

with open('newNSbyID.txt') as f:
    count = 0
    for line in f:
        count += 1
        if count <= 3:
            continue
        NSName = line[:line.find(':')]
        domains = line[line.find(':')+1 : ].split(',')
        domainsByNS[NSName] = {}
        for domain in domains:
            domainsByNS[NSName][domain] = True

# find new NS by domains
with open ('/data1/nsrg/kwang40/fullData/2019-03-03/RR.json') as f:
    for line in f:
        parseRR(line)

for k,v in newDomains.items():
    newDomains[k] = list(set(v))

sorted_Domains = sorted(newDomains.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('newDomainsByNS.txt', sorted_Domains)
