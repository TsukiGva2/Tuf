from collections import deque
from sys import argv, exit
import re

full = {}
prec = {}
strs = {}
tdpn = {}
stck = deque()
utks = {}
ufun = {}
sbuf = ""
undefs = deque()
sstk = [False, 0]
is_in_def = [False, "none"]

def setbuf(word):
    global sbuf
    string = re.search("\$(.+?)\$", word)
    if string != None:
        sbuf = strs[int(string.group(1))]
    else:
        return False
    return True

def getasc():
    if sbuf != "":
        for char in sbuf:
            if sstk[0] == False:
                stck.append(ord(char))
    return True

def defun():
    global is_in_def
    if not is_in_def[0] and undefs:
        neword = str(undefs.pop())
        is_in_def = [True, neword]
        ufun[neword] = []
    return True

_reserved = {"def":defun,"ASC":getasc,"LEN":getbuflen}

if len(argv) < 2:
    print("too few arguments! Usage: python stuff.py -f somefile.tuf")
    exit(1)

elif "-f" not in argv:
    print("no \"-f\" option supplied! use: python stuff.py -f somefile.tuf")
    exit(1)

with open(argv[argv.index("-f")+1]) as f:
    code = f.read()

for ln, pl in enumerate(code.splitlines()):
    linum = ln+1
    if re.search("^\\s*\\t*$",pl) != None:
        continue
    if "#" in pl:
        line = pl.strip(pl[pl.index("#"):])
    else:
        line = pl
    line = line.replace("$",'')
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
            full[linum] = line.replace(quot.group(),"$" + str(linum) + "$").split()
        else:
            full[linum] = full[linum].replace(quot.group(),"$" + str(linum) + "$").split()
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

def execute(word):
    global is_in_def
    if not is_in_def[0]:
        if re.search("^\d+$",word) != None:
            if sstk[0] == False:
                stck.append(int(word))
            else:
                utks[sstk[1]].append(int(word))
            return True
        else:
            if word in _reserved:
                _reserved[word]()
            elif word in ufun:
                for wd in ufun[word]:
                    execute(wd)
            elif "$" in word:
                setbuf(word)
    else:
        if word != "endef":
            ufun[is_in_def[1]].append(word)
        else:
            is_in_def[0] = False

for line in full.keys():
    for word in full[line]:
        if word not in _reserved and word not in ufun:
            undefs.append(word)
        if "-p" in argv or "--step-mode" in argv:
            execute(word)
            print("stack: " + str(stck))
            print("functions: " + str(ufun))
            raw_input()
        else:
            execute(word)

print("\nuser created stacks: " + str(utks))
print("\nstack: " + str(stck))
