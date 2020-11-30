from collections import deque
from sys import argv, exit
import re

undefs       = deque()
full         = {}
strings      = {}
functions    = {"None":["nop"]}
in_defun     = False
curr_defun   = "None"
stacks       = {0:deque()}
selected     = 0
extra_funcs  = [[]]
in_condition = deque([False])
sbuf         = ""
closers      = deque(["ne"])

def setsbuf(word):
    global sbuf
    index = re.search("\$(.+?)\$",word)
    if index != None:
        sbuf = strings[int(index.group(1))][::-1]
    else:
        return False
    return True

def getasc():
    for char in sbuf:
        stacks[selected].append(ord(char))
    return True

def getbuflen():
    stacks[selected].append(len(sbuf))
    return True
    
def emit_stack():
    count = stacks[selected].pop()
    result = ""
    for x in range(count):
        result += chr(stacks[selected].pop())
    print(result)
    return True

def testeq():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    if num1 != num2:
        in_condition.append(True)
        extra_funcs.append([])
        closers.append("qe")

def notest():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    if num1 == num2:
        in_condition.append(True)
        extra_funcs.append([])
        closers.append("en")

def greatest():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    if num1 >= num2:
        in_condition.append(True)
        extra_funcs.append([])
        closers.append("tg")

def letest():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    if num1 <= num2:
        in_condition.append(True)
        extra_funcs.append([])
        closers.append("tl")

def print_last():
    to_print = stacks[selected].pop()
    print(to_print)

def dump_stack():
    for item in stacks[selected]:
        print(item)

def add_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    stacks[selected].append(num1+num2)

def sub_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    stacks[selected].append(num1-num2)

def div_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    if num1 != 0 and num2 != 0:
        stacks[selected].append(num1/num2)

def mul_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    stacks[selected].append(num1*num2)

def pow_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    stacks[selected].append(num1**num2)

def mod_last():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    stacks[selected].append(num1%num2)

def swp():
    current_top = stacks[selected].pop()
    new_top = stacks[selected].pop()
    stacks[selected].append(current_top)
    stacks[selected].append(new_top)

def rot():
    num1 = stacks[selected].pop()
    num2 = stacks[selected].pop()
    num3 = stacks[selected].pop()
    stacks[selected].extend([num1,num2,num3])
    
def popall():
    for x in range(len(stacks[selected])):
        stacks[selected].pop()
        
def defun():
    global in_defun, curr_defun
    if undefs and in_defun != True:
        in_defun = True
        newfunc = undefs.pop()
        functions[newfunc] = []
        curr_defun = newfunc

def select():
    global selected
    stacknum = stacks[selected].pop()
    if stacks[stacknum]:
        selected = stacknum

reserved = {"asc":getasc,"len":getbuflen,"emit":emit_stack,
            "eq":testeq,"ne":notest,"gt":greatest,"lt":letest,
            ".":print_last,"dumps":dump_stack,"add":add_last,
            "sub":sub_last,"pow":pow_last,"div":div_last,
            "mul":mul_last,"mod":mod_last,"pop":lambda: stacks[selected].pop(),
            "dup":lambda: stacks[selected].append(stacks[selected][-1]),
            "swap":swp,"rot":rot,
            "popall":popall,"new":lambda: stacks.append(deque()),
            "select":select,"def":defun,"nop":lambda: 1+1}

def execute(word):
    global in_defun
    if not in_defun and not in_condition[-1]:
        isnum = re.search("^[+-]?[0-9]+$",word)
        if isnum:
            stacks[selected].append(int(word))
        elif word in reserved:
            reserved[word]()
        elif word in functions:
            for wd in functions[word]:
                execute(wd)
        elif "$" in word:
            setsbuf(word)
        else:
            undefs.append(word)
        
    else:
        if not in_defun:
            if word != closers[-1]:
                extra_funcs[-1].append(word)
            else:
                closers.pop()
                in_condition.pop()
        else:
            if word == "endef":
                in_defun = False
            else:
                functions[curr_defun].append(word)

# NOTE this part of the code is still ugly.
# -------------------------------------------
if len(argv) < 2 or "-f" not in argv:
    print("Usage: python tuf.py -f file.tuf")
    exit(1)

with open(argv[argv.index("-f")+1]) as fp:
    code = fp.read()
# -------------------------------------------

# preprocessing
for linum, line in enumerate(code.splitlines()):
    comment = re.search("\#(.*)",line)
    if comment != None:
        line = line.replace(comment.group(),"")
    if re.search("^\s*\t*$",line) != None:  # match 'empty' string
        continue
    # regexes that only iq > 420 can read (obviously not me)
    is_string      = re.search("\"(.+?)\"",line)
    has_precedence = re.search("\((.+?)\)",line)
    postpost       = re.search("\~[A-Za-z]+",line)
                     # this will match -> (anything here)
    
    cut            = re.findall("\_(.+?)\_",line) # match _this_
    # end of regexes
    
    line = line.replace("$","")

    for x in cut:
        line = line.replace("_"+x+"_","")

    if is_string != None:
        strings[linum] = is_string.group(1)
        line = line.replace(is_string.group(),'$' + str(linum) + '$')
        has_precedence = re.search("\((.+?)\)",line)
            # i dont know why but the code breaks without that line

    if has_precedence != None:
        # moving strings around
        line = has_precedence.group(1) + " " + line.replace(has_precedence.group(),"") # string + string = bad code
    if postpost != None:
        # moving strings around again
        line = line.replace(postpost.group(),"") + " " + postpost.group()
        line = line.replace("~","")
    
    full[linum] = line.split()

for line in full.keys():
    for word in full[line]:
        execute(word.lower())
print("execution reached End Of File, here are the results...\nstacks: " + str(stacks).replace("deque","") + "\nfunctions: " + str(functions) + "\nunused code: " + str(extra_funcs))
