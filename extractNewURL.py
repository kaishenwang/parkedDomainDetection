import sys

with open (sys.argv[2]) as f:
    lines = f.readlines()
for i in range(50):
    line = lines[i]
    print(line[:line.find('(')])
