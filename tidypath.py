#!/usr/bin/env python

"""tidypath -- remove duplicate elements from the PATH

Usage: tidypath [--help|-help|-h]

It assembles a new path list from the old path, discarding any elements it has
already found.

Unless printing out this help, prints out the resultant PATH.

For the moment, only works on $PATH -- if necessary, add switches (as in
``showpath``) to specify which path variable to work with.
"""

import sys
import os
import string
import sets

if os.name == "nt":
    PATH_DELIM = ";"
else:
    PATH_DELIM = ":"

def get_path(pathname):
    return string.split(os.environ[pathname],PATH_DELIM)

def tidy_path(pathname):
    orig_path = get_path(pathname)
    elements = sets.Set()
    path = []

    for item in orig_path:
        if item not in elements:
            path.append(item)
            elements.add(item)

    return string.join(path,PATH_DELIM)


# ------------------------------------------------------------
def main():
    """Do it."""

    arg_list = sys.argv[1:]

    pathname = "PATH"

    if arg_list:
        print __doc__
    else:
        print tidy_path(pathname)


# ------------------------------------------------------------
# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()
