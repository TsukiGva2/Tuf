from collections import deque
from sys import argv, exit
import re

full = {}
prec = {}
strs = {}
tdpn = {}
stck = deque()
utks = {}

if len(argv) < 2:
    print("too few arguments! Usage: python stuff.py -f somefile.tuf")
    exit(1)

elif "-f" not in argv:
    print("no \"-f\" option supplied! use: python stuff.py -f somefile.tuf")
    exit(1)

with open(argv[argv.index("-f")+1]) as f:
    code = f.read()

for ln, line in enumerate(code.splitlines()):
    linum = ln+1
    if line.startswith("#") or re.search("^\\s*\\t*$",line) != None:
        continue
    paren = re.search("\((.+?)\)",line)
    quot = re.search("\"(.+?)\"",line)
    if quot!=None and re.search("\((.+?)\)",line.strip(quot.group()))==None:
        paren = None
    if paren != None:
        prec[linum] = paren.group(1)
        if quot == None:
            full[linum] = (prec[linum] + " " + line.replace(paren.group(),"")).split()
            continue
        else:
            full[linum] = prec[linum] + " " + line.replace(paren.group(),"")
    if quot != None:
        strs[linum] = quot.group(1)
        if paren == None:
            full[linum] = line.replace(quot.group(),"$").split()
        else:
            full[linum] = full[linum].replace(quot.group(),"$").split()
        continue
    full[linum] = line.split()

if "-d" in argv or "--debug" in argv:
    for item in full.items():
        print(item)
    print("\nstrings: " + str(strs))
    print("\nprecedence operations: " + str(prec))
    print("\nstack: " + str(stck))
    print("\ntime dependent operations: " + str(tdpn))
    print("\nuser created stacks: " + str(utks))

for line, op in full.keys(), full.items():

