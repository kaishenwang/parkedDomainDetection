import re
from collections import defaultdict
import sys

URLs = defaultdict(list)
endingChars = [')', '\"', ' ', '=', '\\', '}']
errorStr = '\"http\":{}},\"error\":'

def find_all(a_str, sub):
    start = 0
    res = []
    while True:
        start = a_str.find(sub, start)
        if start == -1: break
        res.append(start)
        start += len(sub)
    return res

def parse(line, hostName):
    if line.find(errorStr) != -1:
        return
    for beginStr in ['http://','https://']:
        urlIdxs = find_all(page, beginStr)
        for urlIdx in urlIdxs:
            endIdx = 0
            for i in range(7, 30):
                endIdx = urlIdx + i
                if endIdx >= len(page):
                    break
                if page[endIdx] in endingChars:
                    break
            url = page[urlIdx : endIdx]
            if url.find(hostName) == -1:
                URLs[url].append(domainName)

def writeResult(fName, d):
    with open(fName, 'w') as f:
        for k,v in d:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)):
                f.write(v[idx] + ',')
            f.write('\n')

domainName = ''
with open(sys.argv[1]) as infile:
    for line in infile:
        if line[:7] != '{\"ip\":\"':
            domainNameStart = line.find('domain') + 9
            domainNameEnd = line.find('\"', domainNameStart)
            domainName = line[domainNameStart : domainNameEnd]
        parse(line, domainName)


for k,v in URLs.items():
    URLs[k] = list(set(v))
sorted_list = sorted(URLs.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('newIDURL.txt', sorted_list)
