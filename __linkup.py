#! /usr/bin/env python

"""Make links to these programs from ${HOME}/bin

Find all of the Python scripts in this directory (except this one), and make
soft links to them, but without the trailing '.py'
"""

import sys
import os

def linkup():
    home = os.path.expandvars("${HOME}")

    bindir = os.path.join(home, "bin")
    if not os.path.exists(bindir):
        print 'Creating', bindir
        os.mkdir(bindir)

    this_dir, this_file = os.path.split(__file__)
    this_dir = os.path.abspath(this_dir)

    files = os.listdir(this_dir)
    files.sort()
    for name in files:
        if name in (this_file, 'readme.rst'):
            print 'Ignoring', name
            continue

        if name[-1] in ('~', '#'):
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

        this = os.path.join(this_dir, name)
        that = os.path.join(bindir, usename)

        if os.path.isdir(this):
            print 'Ignoring directory', name
            continue

        try:
            os.symlink(this, that)
            print 'Linked %s to %s'%(that, this)
        except OSError as e:
            if e.errno == 17:
                print 'Entry already exists for',usename
            else:
                print e, base

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        linkup()
    else:
        print __doc__

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
