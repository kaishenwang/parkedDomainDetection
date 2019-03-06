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

def parse(page):
    if page.find(errorStr) != -1:
        return
    domainNameStart = page.find('domain') + 9
    domainNameEnd = page.find('\"', domainNameStart)
    domainName = page[domainNameStart : domainNameEnd]
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
            URLs[page[urlIdx : endIdx]].append(domainName)

def writeResult(fName, d):
    with open(fName, 'w') as f:
        for k,v in d:
            f.write(k + '(' + str(len(v)) + '):' )
            for idx in range(len(v)):
                f.write(v[idx] + ',')
            f.write('\n')

singlePage = ''
with open(sys.argv[1]) as infile:
    for line in infile:
        if line[:7] != '{\"ip\":\"':
            singlePage += line
        else:
            parse(singlePage)
            singlePage = ''

parse(singlePage)

for k,v in URLs.items():
    URLs[k] = list(set(v))
sorted_list = sorted(URLs.items(), key=lambda x: len(x[1]), reverse=True)
writeResult('newIDURL.txt', sorted_list)
