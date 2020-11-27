from collections import deque
from sys import argv, exit
import re

full        = {}
strings     = {}
functions   = {}
in_defun    = False
stacks      = {0:deque()}
selected    = 0
extra_funcs = [[]]
tests       = [[False,"0 1 ne"]]
sbuf        = ""

def setsbuf(word):
    global sbuf
    index = re.search("\$(.+?)\$")
    if index != None:
        sbuf = strings[int(string.group(1))][::-1]
    else:
        return False
    return True

reserved = {"ASC":getasc,"LEN"|}

def execute(word):
    if not in_defun:
        if word in reserved:
            reserved[word]()
        if word in functions:
            execute(functions[word])
        if "$" in word:
            setsbuf(word)

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

    full[linum] = line.split()

for word in full.items():
    if "--debug" in argv:
        print(word)
    execute(word)
