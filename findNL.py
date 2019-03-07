import sys

prevLine = ''
with open(sys.argv[1]) as infile:
    for line in infile:
        if line[:7] == '{\"ip\":\"':
            prevLine = line
        else:
            print(prevLine + line)
            break
