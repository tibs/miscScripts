#!/usr/bin/env python3

"""Report on indentation policies in a file

Usage: check_indent.py file [file ...]
"""

import sys
import os

def check(ff,name):
    noindent   = 0
    justspaces = 0
    justtabs   = 0
    mixed      = 0
    othertabs  = 0
    for line in ff:
        restofline = line.lstrip()
        leadspaces = line[:-len(restofline)]
        if len(leadspaces) == 0:
            noindent += 1
        elif "\t" in leadspaces:
            if " " in leadspaces:
                mixed += 1
            else:
                justtabs += 1
        else:
            justspaces += 1
        othertabs = "\t" in restofline.rstrip()
    return (name,noindent,justspaces,justtabs,mixed,othertabs)

def main(args):
    """Do it."""

    if len(args) == 0:
        print(__doc__)

    results = []
    maxlen = 0
    for name in args:
        try:
            ff = open(name)
            try:
                results.append(check(ff,name))
            finally:
                ff.close()
            if len(name) > maxlen:
                maxlen = len(name)
        except IOError as detail:
            print("Error processing '%s': %s"%(name,detail))
    print("%*s    total   .......... lines with ...........    other"%(maxlen," "))
    print("%*s    lines   spaces     tabs     both  neither     tabs"%(maxlen," "))
    for name,noindent,justspaces,justtabs,mixed,othertabs in results:
        total = noindent + justspaces + justtabs + mixed
        print("%-*s %8d %8d %8d %8d %8d %8d"%(maxlen,name,total,justspaces,
                justtabs,mixed,noindent,othertabs))

if __name__ == "__main__":
    main(sys.argv[1:])
