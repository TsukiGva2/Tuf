from collections import deque
from sys import argv, exit
from random import randrange
import re

full = {}
prec = {}
strs = {}
stck = {0:deque()}
ufun = {}
sbuf = ""
undefs = deque()
sstk = 0
is_in_condition = deque([[False,False]])
is_in_def = [False, "none"]
conditionals_temp = []
ignore = 0

def prntsome():
    print(str(stck[sstk].pop()))

def emitsome():
    result = ""
    if stck[sstk]:
        length = stck[sstk].pop()
        for x in range(length):
            result += chr(stck[sstk].pop())
        print(result)
    return True

def getbuflen():
    stck[sstk].append(len(sbuf))
    return True

def setbuf(word):
    global sbuf
    string = re.search("\$(.+?)\$", word)
    if string != None:
        sbuf = strs[int(string.group(1))][::-1]
    else:
        return False
    return True

def getasc():
    if sbuf != "":
        for char in sbuf:
            stck[sstk].append(ord(char))
    return True

def defun():
    global is_in_def
    if not is_in_def[0] and undefs:
        neword = str(undefs.pop())
        is_in_def = [True, neword]
        ufun[neword] = []
    return True

def clbuf():
    global sbuf
    sbuf = ""
    return True

def new_stack():
    global stck
    stck[stck[sstk].pop()] = deque()
    return True

def chstack():
    global sstk
    news = stck[sstk].pop()
    try:
        print(stck[news])
        sstk = news
        return True
    except KeyError:
        return False

def s_add():
    num1 = stck[sstk].pop()
    num2 = stck[sstk].pop()
    stck[sstk].append(num1 + num2)
    return True

def s_sub():
    num1 = stck[sstk].pop()
    num2 = stck[sstk].pop()
    stck[sstk].append(num1 - num2)
    return True

def s_mul():
    num1 = stck[sstk].pop()
    num2 = stck[sstk].pop()
    stck[sstk].append(num1 * num2)
    return True

def s_div():
    num1 = stck[sstk].pop()
    num2 = stck[sstk].pop()
    if num2 != 0 and num1 != 0:
        stck[sstk].append(num1 / num2)
    else:
        print("zero division error")
        return False
    return True

def s_pow():
    num1 = stck[sstk].pop()
    num2 = stck[sstk].pop()
    stck[sstk].append(num1 ** num2)
    return True

def conditional(word):
    conditionals_temp.append([])
    if "=" in word and int(re.search("\d+",word).group()) == stck[sstk][-1]:
        is_in_condition.append([True,True])
    else:
        is_in_condition.append([True,False])
    return True

def checkEq(): 
    global ignore # gambiarra merda, mudar isso um dia.
    """                 .ROGER.
    --- esse comando e estruturado como 'eq (1 2)'...
    ... 1 e 2 sao colocados na stack e entao a igualdade...
    ... entre eles e verificada. -- teclado sem acentos :p --
                        .ROGER.                         """
    if stck[sstk].pop() != stck[sstk].pop():
        ignore += 1

def skipp():
    if stck[sstk]:


_reserved = {"def":defun,"ASC":getasc,"LEN":getbuflen
        ,"emit":emitsome,".":prntsome,"CB":clbuf
        ,"new":new_stack,"select":chstack,"add":s_add
        ,"sub":s_sub,"mul":s_mul,"div":s_div,"pow":s_pow
        ,"eq":checkEq}

if len(argv) < 2:
    print("too few arguments! Usage: python tuf.py -f somefile.tuf")
    exit(1)

elif "-f" not in argv:
    print("no \"-f\" option supplied! use: python tuf.py -f somefile.tuf")
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
    print("\nstacks: " + str(stck))

def execute(word):
    global is_in_def, is_in_condition, ignore
    if ignore <= 0:
        if is_in_condition[-1][0]:
            if word == "]":
                if is_in_condition[-1][1]:
                    is_in_condition.pop()
                    for wd in conditionals_temp[-1]: 
                        execute(wd)
                    conditionals_temp.pop()
            else:
                conditionals_temp[-1].append(word)
            print(is_in_condition)
        if not is_in_def[0] and not is_in_condition[-1][0]:
            if re.search("^\d+$",word) != None:
                stck[sstk].append(int(word))
                return True
            else:
                if word in _reserved:
                    _reserved[word]()
                elif word in ufun:
                    for wd in ufun[word]:
                        execute(wd)
                elif "$" in word:
                    setbuf(word)
                if "[" in word:
                    conditional(word)
        elif is_in_def[0]:
            if word != "endef":
                ufun[is_in_def[1]].append(word)
            else:
                is_in_def[0] = False
    else:
        ignore -= 1

for line in full.keys():
    for word in full[line]:
        if word not in _reserved and word not in ufun:
            undefs.append(word)
        if "-d" in argv or "--debug" in argv:
            execute(word)
            print("stacks: " + str(stck))
            print("functions: " + str(ufun))
            raw_input()
        else:
            execute(word)

print("\nstacks: " + str(stck))
