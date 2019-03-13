validDomains = {}
with open('validDomains.txt') as f:
    for line in f:
        validDomains[line.rstrip()] = True

oldDomains = {}
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
        if domain in validDomains:
            oldDomains[domain] = True

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
        if domain in validDomains:
            oldDomains[domain] = True

print('Old Domains: ' + str(len(oldDomains)))

overLapCount = 0
with open('domainsByNewUsefulID.txt') as f:
    for line in f:
        domain = line.rstrip()
        if domain in oldDomains:
            overLapCount += 1
print ('Overlap count is ' + str(overLapCount))
