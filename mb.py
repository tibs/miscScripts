#!/usr/bin/env python

"""mb - translate blocks into megabytes, etc.

Usage: mb <number> [<what>]
   or: mb <filename>

where
	<number>   is an integer to convert
	<what>     is "bytes" (the default) or one of "blocks", "Kb",
	           "Mb", or "Gb", indicating what <number> is counting.
		   The size of a block is assumed to be 512 bytes.
        <filename> is the name of a file, whose size should be reported,
	           or a directory, whose contents' size is reported.
"""

import sys
import os
import stat
import string


def dirsize(path):
    """Return the size in bytes of the contents of a directory."""

    os.chdir(path)
    files = os.listdir(".")

    number = 0
    for file in files:
	filepath = os.path.join(path,file)
	fstat = os.stat(filepath)
	number = number + fstat[stat.ST_SIZE]	# add in the file's size
	if os.path.isdir(filepath):
	    number = number + dirsize(filepath)	# add in the directory contents

    return number


def main():
    """Do it."""

    # Extract our arguments

    arg_list = sys.argv[1:]

    # What arguments do we have?

    if len(arg_list) == 0:
	print __doc__
	return

    try:
	number = string.atoi(arg_list[0])
    except:
	path = os.path.expanduser(arg_list[0])
	path = os.path.expandvars(path)
	if path[0] != "/":
	    path = os.path.join(os.getcwd(),path)
	if os.path.exists(path):
	    if os.path.isdir(path):
		number = dirsize(path)
		print "Directory",path,"contains:"
		print "     ",
	    else:
		fstat  = os.stat(path)		# don't follow links
		number = fstat[stat.ST_SIZE]	# assume size in bytes
		print "File",path,"has size:"
		print "     ",
	else:
	    print __doc__
	    return

    if len(arg_list) > 1:
	what = string.lower(arg_list[1])
	if what == "byte" or what == "bytes":
	    pass
	elif what == "block" or what == "blocks":
	    number = number * 512L
	elif what == "kb":
	    number = number * 1024L
	elif what == "mb":
	    number = number * 1024*1024L
	elif what == "gb":
	    number = number * 1024*1024*1024L
	else:
	    print __doc__
	    return

    kb = number / (1024.0)
    mb = number / (1024*1024.0)
    gb = number / (1024*1024*1024.0)

    if number == 1:
	print "1 byte =",
    else:
	print number,"bytes =",

    print "%.3f Kb"%kb,

    if mb > 0.001:
	print "= %.3f Mb"%mb,
	if gb > 0.001:
	    print "= %.3f Gb"%gb,

    print


# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# [X]Emacs local variables declaration - place us into python mode
# Local Variables:
# mode:python
# py-indent-offset:4
# End:
