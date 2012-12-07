#! /usr/bin/env python

"""Make links in the directory above this one.

Find all of the Python scripts in this directory (except this one), and make
soft links to them in the directory above, but without the trailing '.py'
"""

import sys
import os

def linkup():
    this_dir, this_file = os.path.split(__file__)
    this_dir = os.path.abspath(this_dir)
    parent_dir = os.path.split(this_dir)[0]

    files = os.listdir(this_dir)
    files.sort()
    for name in files:
        if name in (this_file, 'readme.rst'):
            print 'Ignoring', name
            continue

        if name[-1] in ('~', '#'):
            print 'Ignoring', name
            continue

        full_path = os.path.join(this_dir, name)
        if os.path.isdir(full_path):
            print 'Ignoring', name
            continue

        base, ext = os.path.splitext(name)

        if ext in ('.swp', '.swo'):
            print 'Ignoring', name
            continue

        if ext == ".py":
            usename = base
        else:
            usename = name

        try:
            os.symlink(full_path,
                       os.path.join(parent_dir, usename))
            print 'Linked %s as ../%s'%(name, usename)
        except OSError as e:
            if e.errno == 17:
                print 'Entry already exists for',base
            else:
                print e, base

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        linkup()
    else:
        print __doc__

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
