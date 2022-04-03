#!/usr/bin/env python3

"""Find and delete all files ending in "~" (i.e., [X]Emacs and vim backup
files) in the given directory (directories) and its (their) subdirectories.

Usage:
    remove_twiddle_files [<switches>] <dir> [<dir> ...]

If "-v" is given, announcements will be given for each directory checked.
If "-n" is given (for "no-effect"), then no files will actually be deleted.

If "-swp" is given, ".swp" and ".swo" files will also be deleted.
If "-dep" is given, ".depend" files will also be deleted.
If "-all" is given, then all the above extra files to delete are deleted.

If "-tag" is given, "tags" tiles will also be deleted. This is not included
in "-all", because it is not *quite* the same sort of thing.

If "-pyc" is given, then ".pyc" files will also be deleted. Again, this is
not included in "-all".

If "-notwiddle" is given, then files ending in "~" will not be deleted.

Note: does not follow or remove links. Also, does not look inside ".bzr",
".svn", ".git", ".hg" or ".tox" directories.
"""

import sys
import os
import errno

class Remove(object):
    twiddle = True
    swp = False
    dep = False
    tag = False
    pyc = False

def process(dirname, remove, pretend=False, verbose=True):
    if verbose:
        print("Processing %s"%dirname)
    files = os.listdir(dirname)
    files.sort()
    for name in files:
        what = os.path.join(dirname,name)
        if os.path.islink(what):
            continue
        if os.path.isdir(what):
            if name not in (".bzr", ".svn", ".git", ".hg", ".tox"):
                process(what, remove, pretend, verbose)
        else:
            if (remove.twiddle and name[-1] == "~") or \
               (remove.swp and name[-4:] in (".swp", ".swo")) or \
               (remove.dep and name == ".depend") or \
               (remove.tag and name == "tags") or \
               (remove.pyc and name.endswith(".pyc")):
                if pretend:
                    print("  'Deleting'",what)
                else:
                    print("  Deleting",what)
                    try:
                        os.remove(what)
                    except OSError as e:
                        if e.errno == errno.EBUSY:
                            print("  ...which is in use (EBUSY), so not deleting it")
                        else:
                            raise

def main():
    pretend = False
    remove = Remove()
    verbose = False
    directories = []
    arg_list = sys.argv[1:]
    if len(arg_list) < 1:
        print(__doc__)
        return

    while arg_list:
        word = arg_list.pop(0)
        if word in ["-help", "-h"]:
            print(__doc__)
            return
        elif word == "-n":
            pretend = 1
            print("Just pretending")
        elif word == "-notwiddle":
            remove.twiddle = False
        elif word == "-swp":
            remove.swp = True
        elif word == "-dep":
            remove.dep = True
        elif word == "-tag":
            remove.tag = True
        elif word == "-pyc":
            remove.pyc = True
        elif word == "-all":
            remove.swp = True
            remove.dep = True
        elif word == "-v":
            verbose = True
        else:
            directories.append(word)

    if not directories:
        print("No directory specified")
        print()
        print(__doc__)
        return

    print("Looking for", end=' ')
    if remove.twiddle: print("~ files", end=' ')
    if remove.swp: print(".swp files", end= ' ')
    if remove.dep: print(".depend files,", end= ' ')
    if remove.tag: print("tags files", end= ' ')
    if remove.pyc: print(".pyc files", end=' ')
    print("in %s"%(', '.join(directories)))

    for dirname in directories:
        if os.path.isdir(dirname):
            process(dirname, remove, pretend, verbose)
        else:
            if os.path.exists(dirname):
                print("!!! '%s' is not a directory"%dirname)
            else:
                print("!!! Directory '%s' does not exist"%dirname)

if __name__ == "__main__":
    main()
