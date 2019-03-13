validDomains = {}
with open('validDomains.txt') as f:
    for line in f:
        validDomains[line.rstrip()] = True
uniqueDomains = {}
# Token NS
nonValidNS = {}
with open('nonValidTokenNS.txt') as f:
    lines = f.readlines()
for line in lines:
    nonValidNS[line.rstrip()] = True

with open('tokenNS.txt') as f:
    lines = f.readlines()
for line in lines:
    parts = line.rstrip().split(':')
    if parts[0] in nonValidNS:
        continue
    domainsList = parts[1].split(',')
    for domain in domainsList:
        uniqueDomains[domain] = True

# Other NS
with open('otherNS.txt') as f:
    lines = f.readlines()
count = 0
for line in lines:
    count += 1
    if count > 50:
        break
    parts = line.rstrip().split(':')
    if parts[0] in nonValidNS:
        continue
    domainsList = parts[1].split(',')
    for domain in domainsList:
        uniqueDomains[domain] = True

# ID
with open('domainsByFullID.txt') as f:
    for line in f:
        uniqueDomains[line.rstrip()] = True

# New NS
newNS = {}
with open('newNS.txt') as f:
    for line in f:
        newNS[line.rstrip()] = True

with open ('newDomainsByNSTop50.txt') as f:
    for line in f:
        nsName = line[:line.find(':')]
        if nsName not in newNS:
            continue
        domainsList = line[line.find(':') + 1 : ].split(',')
        for domain in domainsList:
            uniqueDomains[domain] = True

with open('fullParkedDomains.txt', 'w') as f:
    for domain in uniqueDomains.keys():
        f.write(domain + '\n')
