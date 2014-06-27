#!/usr/bin/env python

"""Find and delete all files ending in "~" (i.e., [X]Emacs and vim backup
files) in the given directory (directories) and its (their) subdirectories.

Usage:
    remove_twiddle_files [-q] [-p] [-swp] <dir> [<dir> ...]

If "-v" is given, announcements will be given for each directory checked.
If "-p" is given, then no files will actually be deleted.

If "-swp" is given, ".swp" and ".swo" files will also be deleted.
If "-dep" is given, ".depend" files will also be deleted.
If "-all" is given, then all the above extra files to delete are deleted.

If "-tag" is given, "tags" tiles will also be deleted. This is not included
in "-all", because it is not *quite* the same sort of thing.

Note: does not follow or remove links. Also, does not look inside ".bzr",
".svn", ".git" or ".hg" directories.
"""

import sys
import string
import os
import errno

def process(dir,pretend=0,remove_swp=0,remove_dep=0,remove_tag=0,verbose=1):
    if verbose:
        print "Processing %s"%dir
    files = os.listdir(dir)
    files.sort()
    for name in files:
        what = os.path.join(dir,name)
        if os.path.islink(what):
            continue
        if os.path.isdir(what):
            if name not in (".bzr", ".svn", ".git", ".hg"):
                process(what,pretend,remove_swp,remove_dep,verbose)
        else:
            if name[-1] == "~" or \
               (remove_swp and name[-4:] in (".swp", ".swo")) or \
               (remove_dep and name == ".depend") or \
               (remove_tag and name == "tags"):
                if pretend:
                    print "  'Deleting'",what
                else:
                    print "  Deleting",what
                    try:
                        os.remove(what)
                    except OSError as e:
                        if e.errno == errno.EBUSY:
                            print "  ...which is in use (EBUSY), so not deleting it"
                        else:
                            raise

def main():
    pretend = 0
    remove_swp = 0
    remove_dep = 0
    remove_tag = 0
    verbose = 0
    arg_list = sys.argv[1:]
    if len(arg_list) < 1:
	print __doc__
	return

    while len(arg_list) > 0:
        if arg_list[0] in ["-help", "-h"]:
	    print __doc__
	    return
        elif arg_list[0] == "-p":
            pretend = 1
            print "Just pretending"
        elif arg_list[0] == "-swp":
            remove_swp = 1
        elif arg_list[0] == "-dep":
            remove_dep = 1
        elif arg_list[0] == "-tag":
            remove_tag = 1
        elif arg_list[0] == "-all":
            remove_swp = 1
            remove_dep = 1
        elif arg_list[0] == "-v":
            verbose = 1
        else:
            break
        arg_list = arg_list[1:]

    if len(arg_list) == 0:
        print "No directory specified"
        print
        print __doc__
        return

    print "Looking for ~ files",
    if remove_swp: print ".swp files",
    if remove_dep: print ".depend files,",
    if remove_tag: print "tags files",
    print

    for dir in arg_list:
	if os.path.exists(dir) and os.path.isdir(dir):
            process(dir,pretend,remove_swp,remove_dep,remove_tag,verbose)
	else:
	    if not os.path.exists(dir):
		print "!!! Directory '%s' does not exist"%dir

if __name__ == "__main__":
    main()
