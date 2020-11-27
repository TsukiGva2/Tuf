from collections import deque
from sys import argv, exit
import re

full        = {}
strings     = {}
functions   = {}
stacks      = {0:deque()}
extra_funcs = [[]]
tests       = [[False,"0 1 ne"]]

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

    for x in cut:
        line = line.replace(x,"")
    
    line = line.replace("_","")

    if is_string != None:
        strings[linum] = is_string.group(1)
        line = line.replace(is_string.group(),'$' + str(linum) + '$')
        has_precedence = re.search("\((.+?)\)",line)
            # i dont know why but the code breaks without that line

    if has_precedence != None:
        # moving strings around
        line = has_precedence.group(1) + " " + line.replace(has_precedence.group(),"") # string + string = bad code

    full[linum] = line.split()

if "--debug" in argv:
    for word in full.items():
        print(word)
