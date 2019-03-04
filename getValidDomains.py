import sys

with open(sys.argv[1]) as infile:
    for line in infile:
        if line[:7] != '{\"ip\":\"':
            continue
        domainNameStart = line.find('domain') + 9
        domainNameEnd = line.find('\"', domainNameStart)
        print (line[domainNameStart:domainNameEnd])
