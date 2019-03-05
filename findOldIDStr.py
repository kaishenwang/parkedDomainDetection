import sys
import re

#python findOldIDStr.py oldIDStr.txt /data1/nsrg/kwang40/fullData/2019-03-03/banners.json
IDs = {}
IDStrs = {}
errorStr = '\"http\":{}},\"error\":'
def parse(page):
    if page.find(errorStr) != -1:
        return
    domainNameStart = page.find('domain') + 9
    domainNameEnd = page.find('\"', domainNameStart)
    domainName = page[domainNameStart:domainNameEnd]
    for ID in IDs.keys():
        if re.match(ID, page, flags=0) != None:
            IDs[ID].append(domainName)
    for ID in IDStrs.keys():
        if page.find(ID) != -1:
            IDStrs[ID].append(domainName)

def writeResult(fName, d, d2):
    with open(fName, 'w') as f:
        for k,v in d:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)-1):
                f.write(v[idx] + ',')
            if (len(v) > 0):
                f.write(v[-1] + '\n')
        f.write('\n')
        for k,v in d2:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)-1):
                f.write(v[idx] + ',')
            if (len(v) > 0):
                f.write(v[-1] + '\n')

with open (sys.argv[1]) as f:
    lines = f.readlines()

for i in range(5):
    IDs[lines[i].rstrip()] = []
for i in range(5, len(lines)):
    IDStrs[lines[i].rstrip()] = []

singlePage = ''
with open(sys.argv[1]) as infile:
    for line in infile:
        if line[:7] != '{\"ip\":\"':
            singlePage += line
        else:
            parse(singlePage)
            singlePage = ''

parse(singlePage)

for k,v in IDs.items():
    IDs[k] = list(set(v))
for k,v in IDStrs.items():
    IDStrs[k] = list(set(v))

sorted_list = sorted(IDs.items(), key=lambda x: len(x[1]), reverse=True)
sortedStr_list = sorted(IDStrs.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('oldIDMatchResult.txt', sorted_list, sortedStr_list)
