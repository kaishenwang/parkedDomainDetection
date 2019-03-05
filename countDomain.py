tokenNSFName = 'tokenNS.txt'
otherNSFName = 'otherNS.txt'
nonValidTokenNSFName = 'nonValidTokenNS.txt'
nonValidOtherNSFName = 'nonValidOtherNS.txt'

nonValidNS = {}
with open(nonValidTokenNSFName) as f:
    lines = f.readlines()
for line in lines:
    nonValidNS[line.rstrip()] = True

with open(nonValidOtherNSFName) as f:
    lines = f.readlines()
for line in lines:
    nonValidNS[line.rstrip()] = True

domains = {}
with open(tokenNSFName) as f:
    lines = f.readlines()
for line in lines:
    parts = line.rstrip().split(':')
    if parts[0] in nonValidNS:
        continue
    domainsList = parts[1].split(',')
    for domain in domainsList:
        domains[domain] = True

with open(otherNSFName) as f:
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
        domains[domain] = True

print (len(domains.keys()))
