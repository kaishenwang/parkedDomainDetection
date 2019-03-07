import sys
import re

#python findOldIDStr.py oldIDStr.txt /data1/nsrg/kwang40/fullData/2019-03-03/banners.json
IDs = {}
IDStrs = {}
errorStr = '\"http\":{}},\"error\":'
uniqueDomains = {}
def parse(line, domain):
    if line.find(errorStr) != -1:
        return
    for ID in IDs.keys():
        if re.match(ID, line, flags=0) != None:
            IDs[ID].append(domain)
            uniqueDomains[domain] = True
    for ID in IDStrs.keys():
        if line.find(ID) != -1:
            IDStrs[ID].append(domain)
            uniqueDomains[domain] = True

def writeResult(fName, d, d2):
    with open(fName, 'w') as f:
        f.write(str(len(uniqueDomains)) + '\n')
        for k,v in d:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)):
                f.write(v[idx] + ',')
            f.write('\n')
        f.write('\n')
        for k,v in d2:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)):
                f.write(v[idx] + ',')
            f.write('\n')

with open (sys.argv[1]) as f:
    lines = f.readlines()

for i in range(5):
    IDs[lines[i].rstrip()] = []
for i in range(5, len(lines)):
    IDStrs[lines[i].rstrip()] = []

domainName = ''

with open(sys.argv[2]) as infile:
    for line in infile:
        if line[:7] == '{\"ip\":\"':
            domainNameStart = line.find('domain') + 9
            domainNameEnd = line.find('\"', domainNameStart)
            domainName = line[domainNameStart : domainNameEnd]
        parse(line, domainName)


for k,v in IDs.items():
    IDs[k] = list(set(v))
for k,v in IDStrs.items():
    IDStrs[k] = list(set(v))

sorted_list = sorted(IDs.items(), key=lambda x: len(x[1]), reverse=True)
sortedStr_list = sorted(IDStrs.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('oldIDMatchResult.txt', sorted_list, sortedStr_list)
