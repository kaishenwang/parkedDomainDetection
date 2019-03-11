with open('nonValidTokenNS.txt') as f:
    lines = f.readlines()
nonValidToken = {}
for line in lines:
    nonValidToken[line.rstrip()] = True

NSs = []
with open('tokenNS.txt') as f:
    for line in f:
        NSName = line[:line.find(':')]
        if NSName not in nonValidToken:
            NSs.append(NSName)

with open('otherNS.txt') as f:
    count = 0
    for line in f:
        count += 1
        if count > 50:
            break
        NSName = line[:line.find(':')]
        NSs.append(NSName)

with open('NSwithSepcialWords.txt', 'w') as f:
    for NS in NSs:
        f.write(NS + '\n')
