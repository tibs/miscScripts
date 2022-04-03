#!/usr/bin/env python3

"""Print out the path (of various sorts)

Usage: %s [ <see below> ]

    Where:
        no arguments    means print out PATH
        -ld             means print out LD_LIBRARY_PATH
        -man            means print out MANPATH
        -python         means print out the Python path
                        (which is related to PYTHONPATH, but likely
                        to be longer to take account of Python's automatic
                        decision of where it's files live)
        -path <what>    means print out the path <what>
                        (assumed to be a colon separated path list on Unix,
                         and a semicolon separated path list on NT)


        -help           prints out this text
        -version        prints out the version information
        -history        prints out the history information

The environment variable used as the path name will be tried in uppercase,
lowercase and capitalised if it is not found as requested.

Path components are listed, and then a note is given of any which are
present more than once.
"""

__version__ = "1.1 (Tibs)"
__history__ = """\
1998-04-21: Created by Tibs
1999-11-05: Now works on Unix and NT
2017-10-12: Assume Python 3 (and do minimal fixes for that)
"""

import sys
import string
import os


if os.name == "nt":
    PATH_DELIM = ";"
else:
    PATH_DELIM = ":"


# ------------------------------------------------------------
def environ(item):
    """Try to cope with case differences in environment variables...

    Returns the actual environment variable it used, and its value
    """

    if item in os.environ:
        return (item,os.environ[item])
    else:
        other = []
        up = item.upper()
        if up != item: other.append(up)
        down = item.lower()
        if down != item: other.append(down)
        cap = item.capitalize()
        if cap != item: other.append(cap)

        for name in other:
            if name in os.environ:
                return (name,os.environ[name])

        raise KeyError("There is no environment variable %s (also tried %s)" % (item,", ".join(other)))



# ------------------------------------------------------------
def print_usage(argv0):
    script_name = string.split(argv0, os.sep)[-1]
    print(__doc__%(script_name))


def print_envpath(envar):
    try:
        (name,path) = environ(envar)
    except KeyError as what:
        print('KeyError', what)
        return

    print_path(name, path.split(PATH_DELIM))


def print_path(name,path):
    print("Path %s:" % name)
    count = {}
    index = 0
    for item in path:
        index = index + 1
        print("  %2d: %s" % (index,item))
        if item in count:
            count[item] = count[item] + 1
        else:
            count[item] = 1
    for key in sorted(count):
        if count[key] > 1:
            if count[key] == 2:
                print("Item %s occurs twice" % (key))
            else:
                print("Item %s occurs %d times" % (key,count[key]))


# ------------------------------------------------------------
def main():
    """Do it."""

    # Extract our arguments

    arg_list = sys.argv[1:]

    # What arguments do we have?

    if len(arg_list) == 0:
        print_envpath("PATH")
    elif len(arg_list) == 2 and arg_list[0] == "-path":
        print_envpath(arg_list[1])
    elif len(arg_list) > 1:
        print_usage(sys.argv[0])
    elif arg_list[0] == "-help":
        print_usage(sys.argv[0])
    elif arg_list[0] == "-version":
        print("Version:",__version__)
    elif arg_list[0] == "-history":
        print("History:")
        print(__history__)
    elif arg_list[0] == "-ld":
        print_envpath("LD_LIBRARY_PATH")
    elif arg_list[0] == "-man":
        print_envpath("MANPATH")
    elif arg_list[0] == "-python":
        print_path("sys.path",sys.path)
    else:
        print_usage(sys.argv[0])



# ------------------------------------------------------------
# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()
