outputs = []
uniqueDomains = {}
with open('newNSbyID.txt') as f:
    countLine = 0
    countDomains = 0
    for line in f:
        countLine += 1
        if countLine == 51:
            print('First 50 NS contains: ' + str(countDomains))
        NSName = line[:line.find(':')]
        outLine = NSName + ':'
        domains = split(line[line.find(':')+1 : ], ',')
        for domain in domains:
            if domain[-NSName:] == domain:
                continue
            outLine += domain + ','
            if domain not in uniqueDomains:
                countDomains += 1
            uniqueDomains[domain] = True
        if len(outLine) == len(NSName) + 1:
            continue
        outputs.append(outLine)

print ('Total NS counts: ' + str(len(uniqueDomains)))
with open('refinedNewNSbyID.txt', 'w') as f:
    for outLine in outputs:
        f.write(outLine[:-1] + '\n')
