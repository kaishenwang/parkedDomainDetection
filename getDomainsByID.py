uniqueDomains = {}
IDs = []

errorStr = '\"http\":{}},\"error\":'
def parseZgrabJson(line):
    if line.find(errorStr) != -1:
        return
    hostNameStart = line.find('domain') + 9
    hostNameEnd = line.find('\"', hostNameStart)
    hostName = line[hostNameStart:hostNameEnd]
    for ID in IDs:
        if line.find(ID) != -1:
            uniqueDomains[hostName] = True

#read IDs
with open('fullID.txt') as f:
    lines = f.readlines()
IDs = [line.rstrip() for line in lines]

# find all domains found by ID
with open('/data1/nsrg/kwang40/fullData/2019-03-03/banners.json') as f:
    for line in f:
        if len(line) > 6:
            parseZgrabJson(line)

with open('domainsByFullID.txt', 'w') as f:
    for domain in uniqueDomains.keys():
        f.write(domain + '\n')
