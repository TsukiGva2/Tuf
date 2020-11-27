from sys import argv, exit
import re

full = {}
prec = {}
strs = {}
tdpn = {}
stck = []
utks = {}

if len(argv) < 2:
    print("too few arguments! Usage: python stuff.py -f somefile.tuf")
    exit(1)

elif "-f" not in argv:
    print("no \"-f\" option supplied! use: python stuff.py -f somefile.tuf")
    exit(1)

with open(argv[argv.index("-f")+1]) as f:
    code = f.read()

for linum, line in enumerate(code.splitlines()):
    print(linum)
    if line.startswith("#") or re.search("^\\s*\\t*$",line) != None:
        continue
    paren = re.search("\((.+?)\)",line)
    quot = re.search("\"(.+?)\"",line)
    if quot!=None and re.search("\((.+?)\)",line.strip(quot.group()))==None:
        paren = None
    if paren != None:
        prec[linum] = paren.group(1)
        full[linum] = line.strip(paren.group()).split()
        if quot == None:
            prec[linum] = prec[linum].split()
            continue
        else:
            prec[linum] = prec[linum].replace(quot.group(),"$")
        prec[linum] = prec[linum].split()
    if quot != None:
        strs[linum] = quot.group(1)
        full[linum] = line.strip(quot.group()).split()
        continue
    full[linum] = line.split()

print(full)
print("\nstrings: " + str(strs))
print("\nprecedence operations: " + str(prec))
print("\nstack: " + str(stck))
print("\ntime dependent operations: " + str(tdpn))
print("\nuser created stacks: " + str(utks))
