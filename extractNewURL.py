import sys

with open (sys.argv[1]) as f:
    lines = f.readlines()
for i in range(50):
    line = lines[i]
    print(line[:line.find('(')])
