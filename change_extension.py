#!/usr/bin/env python3

"""Change extensions of all matched files in a directory.

Usage: %s ext1 ext2 [dir1 [dir2 [...]]]

    Where "ext1" is the extension files currently have, "ext2" is the
    extension they should have, and "dir<n>" is a list of directories
    in which to perform the renaming (defaulting to the current directory).

    Note that both "ext1" and "ext2" may contain embedded dots (for
    instance, to allow one to replace "fred.tar.gz" with "fred.tgz").

    If "ext2" is the empty string (""), then the files will end up with
    no extension.

    Note that if either of  "ext1" or "ext2" is non-empty, and does not
    start with a ".", then a "." will be prepended.

Original code by Tibs:
    Tony J. Ibbs (Tibs) <tibs@tibsnjoan.co.uk>

Handling extensions with dots in by Dinu:
    Dinu C. Gherman <gherman@europemail.com>
    http://starship.skyport.net/crew/gherman
"""

__version__ = "1.1 (1998-04/Dinu)"
__history__ = """\
Created by Tibs at some time in history
Amended by Dinu 1998-04 to:
    1) handle extensions containing embedded dots
    2) look up the command name used when printing out help
Amended by Tibs 1998-04 as well, mangling Dinu's code (so don't blame
him if I got it wrong again!)

Updated for Python 3, 2022-04-03
"""


import sys
import os


def multiSplitText(aString, anExt):
    """Split off a multi-part extension from a string's tail."""

    if anExt == '':
        return os.path.splitext(aString)

    e  = ''
    root = s1 = aString
    while 1:
        if e == anExt:
            break   # at this point, root == s1, I believe
        root,ext = os.path.splitext(s1)
        if ext == '':
            break
        e = ext + e
        s1 = root
    return root,e


def doit(dir,ext1,ext2):
    """Rename files in "dir" with extension "ext1" to extension "ext2"."""

    print("Directory",dir)

    files = os.listdir(dir)
    files.sort()

    for file in files:
        root,ext = multiSplitText(file, ext1)

        if ext == ext1:
            oldfile = os.path.join(dir,file)
            newfile = os.path.join(dir,root+ext2)
            print("Renaming %s to %s"%(oldfile,newfile))

            if os.path.exists(os.path.join(dir,newfile)):
                print("*** Unable to rename %s to %s (already exists"%(oldfile, newfile))
            else:
                try:
                    os.rename(oldfile,newfile)
                except:
                    print("*** Unable to rename %s"%oldfile)


def main():
    """Called from the toplevel."""

    # Extract our arguments

    arg_list = sys.argv[1:]

    # What arguments do we have?

    if len(arg_list) < 2:
        scriptName = os.path.split(sys.argv[0])[-1]
        print(__doc__ % scriptName)
        return

    ext1 = arg_list[0]
    ext2 = arg_list[1]

    # Make sure the extensions start with "."
    # (unless they're the empty string)

    if len(ext1) != 0 and ext1[0] != ".":
        ext1 = "."+ext1

    if len(ext2) != 0 and ext2[0] != ".":
        ext2 = "."+ext2

    # Sort out which directories we want

    dirs = arg_list[2:]
    if len(dirs) == 0:
        dirs = ["."]

    # And process each of them

    for dir in dirs:
        # Let's be cautious...

        if os.path.isdir(dir):
            doit(dir,ext1,ext2)
        else:
            print("%s is not a directory"%dir)


# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()
