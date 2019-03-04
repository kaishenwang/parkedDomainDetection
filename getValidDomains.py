import sys

with open(sys.argv[1]) as infile:
    for line in infile:
        domainNameStart = line.find('domain') + 9
        domainNameEnd = line.find('\"', domainNameStart)
        print (domain)
