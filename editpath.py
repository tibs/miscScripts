#!/usr/bin/env python

"""editpath -- return an altered version of the PATH

Usage: editpath <operation> [<operation> ...] <element>

where <operation> is:

        remove    -- remove the first occurrence of <element> from the path
        removeall -- remove all occurrences of <element> from the path
        prepend   -- add <element> to the start of the path
        append    -- add <element> to the end of the path

If more than one <operation> is specified, then they will be applied in the
order given (but all using the same <element>). Thus, to remove all previous
occurrences of "fred" from the path, and then add a single occurrence to the
end, one would use::

        editpath removeall append fred

After doing all of the requested operations, it prints out the resultant PATH.

For the moment, only works on $PATH -- if necessary, add switches (as in
``showpath``) to specify which path variable to work with.
"""

import sys
import os
import string
import stat
import re

if os.name == "posix":
    PATH_DELIM = ":"
else:
    PATH_DELIM = ";"

# ------------------------------------------------------------
def main():
    args = sys.argv[1:]

    pathname = "PATH"

    if len(args) < 2:
        print __doc__
        return

    if args[0] in ("-h", "-help", "--help"):
        print __doc__
        return

    operations = args[:-1]
    element = args[-1]

    pathlist = string.split(os.environ[pathname],PATH_DELIM)

    for operation in operations:
        if operation == "append":
            pathlist.append(element)
        elif operation == "prepend":
            pathlist = [element] + pathlist
        elif operation == "remove":
            try:
                pathlist.remove(element)
            except ValueError:
                pass
        elif operation == "removeall":
            try:
                while 1:
                    pathlist.remove(element)
            except ValueError:
                pass
        else:
            # This is a bit awkward - should we ignore things we don't recognise
            # (and thus give an incorrect/unexpected result), or grumble (and thus
            # return a string that is not a valid path).
            print "*** Unexpected operation '%s'"%operation
            return

    print string.join(pathlist,PATH_DELIM)


# ------------------------------------------------------------
# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# vim: set filetype=python expandtab tabstop=4 shiftwidth=4:
# [X]Emacs local variables declaration - place us into python mode
# Local Variables:
# mode:python
# py-indent-offset:4
# End:
