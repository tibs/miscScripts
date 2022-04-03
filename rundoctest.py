#! /usr/bin/env python3
"""Run the doctest on a text file

    Usage: rundoctest.py  [<file>]
           rundoctest.py -m <module>

[<file>] defaults to ``test.txt``

<module> is a Python module.

Optionally specify -v, -verbose, for more information.
"""

import sys
import doctest

def main():
    args = sys.argv[1:]
    filename = None
    module = None
    verbose = False

    for word in args:
        if word in ("-v", "-verbose"):
            verbose = True
        elif word in ("-h", "-help", "/?", "/help", "--help"):
            print(__doc__)
            return
        elif word == '-m':
            module = args[1]
        else:
            if filename:
                print("Filename '%s' already specified"%filename)
                return
            else:
                filename = word


    # I want to be able to use the "with" statement in the doctests.
    # It's not possible to use "from __future__ import with_statement"
    # in doctests as such. Instead, one has to add the resulting globals
    # to the doctest context. Which seems to be done as follows:
    import __future__
    extraglobs={'with_statement':__future__.with_statement}


    if module:
        m = __import__(module)

        (failures,tests) = doctest.testmod(m,verbose=verbose,
                                           extraglobs=extraglobs)
    else:
        if not filename:
            filename = "test.txt"

        (failures,tests) = doctest.testfile(filename,verbose=verbose,
                                            extraglobs=extraglobs)

    testword = "test"
    if tests != 1: testword = "tests"
    failword = "failure"
    if failures != 1: failword = "failures"
    print()
    print("File %s: %d %s, %d %s"%(filename,tests,testword,failures,failword))
    print()
    if failures == 0:
        print('The little light is GREEN')
    else:
        print('The little light is RED')

if __name__ == "__main__":
    main()
