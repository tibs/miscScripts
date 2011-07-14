#! /usr/bin/env python

"""Make links in the directory above this one.

Find all of the Python scripts in this directory (except this one), and make
soft links to them in the directory above, but without the trailing '.py'
"""

import os

def linkup():
    this_dir, this_file = os.path.split(__file__)
    this_dir = os.path.abspath(this_dir)
    parent_dir = os.path.split(this_dir)[0]

    files = os.listdir(this_dir)
    for name in files:
        if name == this_file:
            print 'Ignoring this file,', name
        elif name.endswith('.py'):
            link = name[:-3]
            print 'Linking %s as ../%s'%(name, link)
            try:
                os.symlink(os.path.join(this_dir, name),
                           os.path.join(parent_dir, link))
            except OSError as e:
                print '..', e

if __name__ == '__main__':
    linkup()

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
