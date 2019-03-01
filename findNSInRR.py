import sys
import re
from collections import defaultdict
# python findNSInRR.py fileName strName

def validChar(c):
    return c.isalnum() or c == '.' or c == '-'

def writeResult(fName, d):
    with open(fName, 'w') as f:
        for k,v in d:
            f.write(k + ':')
            for idx in range(len(v)-1):
                f.write(v[idx] + ',')
            f.write(v[-1] + '\n')

keyStr = sys.argv[2]
keys = keyStr.split(',')

with open(sys.argv[1]) as f:
    lines = f.readlines()

tokenNS = defaultdict(list)
otherNS = defaultdict(list)

for line in lines:
    hostNameEnds = line.find('\"', 9)
    hostName = line[9:hostNameEnds]
    for key in keys:
        idxes = [m.start() for m in re.finditer(key, line)]
        for idx in idxes:
            start = idx -1
            end = idx + len(key)
            token = start >= 0 and end < len(line) and (line[start] == '.' or \
                line[start] == '\"') and (line[end] == '.' or line[end] == '\"')
            while start >= 0 and validChar(line[start]):
                start -= 1
            while end < len(line) and validChar(line[end]):
                end += 1
            if token:
                tokenNS[line[start + 1 : end]].append(hostName)
            else :
                otherNS[line[start + 1 : end]].append(hostName)

tokenDomains = 0
otherDomains = 0
for k,v in tokenNS.items():
    v = set(v)
    if k not in v:
        tokenNS[k] = list(v)
        tokenDomains += len(v)
    else:
        del tokenNS[k]

for k,v in otherNS.items():
    v = set(v)
    if k not in v:
        otherNS[k] = list(v)
        otherDomains += len(v)
    else:
        del otherNS[k]

tokenNSCount = len(tokenNS.keys())
otherNSCount = len(otherNS.keys())
sorted_token = sorted(tokenNS.items(), key=lambda x: len(x[1]), reverse=True)
sorted_others = sorted(otherNS.items(), key=lambda x: len(x[1]), reverse=True)

print("Token NS Count:" + str(tokenNSCount))
print("Other NS Count:" + str(otherNSCount))
print("Token Domain Count:" + str(tokenDomains))
print("Other Domain Count:" + str(otherDomains))

writeResult('tokenNS.txt', sorted_token)
writeResult('otherNS.txt', sorted_others)
