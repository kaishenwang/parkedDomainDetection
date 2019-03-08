import sys
from collections import defaultdict

#python findNewURLMatchDomain.py parkedDomains.txt newIDURL.txt  /data1/nsrg/kwang40/fullData/2019-03-03/banners.json
URLs = []
parkedDomains = {}
newDomains = defaultdict(list)

errorStr = '\"http\":{}},\"error\":'
def parse(line, domain):
    if line.find(errorStr) != -1:
        return
    for url in URLs:
        if line.find(url) != -1:
            newDomains[url].append(domain)

with open (sys.argv[1]) as f:
    lines = f.readlines()
for line in lines:
    parkedDomains[line.rstrip()] = True

with open (sys.argv[2]) as f:
    lines = f.readlines()
for i in range(50):
    line = lines[i]
    URLs.append(line[:line.find(':', 7)])

with open(sys.argv[3]) as infile:
    for line in infile:
        if line[:7] == '{\"ip\":\"':
            domainNameStart = line.find('domain') + 9
            domainNameEnd = line.find('\"', domainNameStart)
            domainName = line[domainNameStart : domainNameEnd]
            if domainName not in parkedDomains:
                parse(line, domainName)

for k,v in newDomains.items():
    newDomains[k] = list(set(v))

with open ('newURLMatchDomains.txt', 'w') as f:
    for url in URLs:
        f.write(url + ':')
        for domain in newDomains[url]:
            f.write(domain + ',')
        f.write('\n')
