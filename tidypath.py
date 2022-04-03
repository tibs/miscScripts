#!/usr/bin/env python3

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

if os.name == "nt":
    PATH_DELIM = ";"
else:
    PATH_DELIM = ":"

def get_path(pathname):
    return os.environ[pathname].split(PATH_DELIM)

def tidy_path(pathname):
    orig_path = get_path(pathname)
    elements = set()
    path = []

    for item in orig_path:
        if item not in elements:
            path.append(item)
            elements.add(item)

    return PATH_DELIM.join(path)


# ------------------------------------------------------------
def main():
    """Do it."""

    arg_list = sys.argv[1:]

    pathname = "PATH"

    if arg_list:
        print(__doc__)
    else:
        print(tidy_path(pathname))


# ------------------------------------------------------------
# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()
