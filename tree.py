#! /usr/bin/env python
# -*- coding: latin-1 -*-

"""Usage: tree.py [-s <dir>] [<directory>]

Directories named by '-s' will not have their content shown
"""

import sys
import os
import stat

INDENT = '    '

def filestr(path, filename, fold_dirs=None):
    """Return a useful representation of a file.

    'path' is the full path of the file, sufficient to "find" it with
    os.stat() (so it may be relative to the current directory).

    'filename' is just its filename, the last element of its path,
    which is what we're going to use in our representation.

    We could work the latter out from the former, but our caller already
    knew both, so this is hopefully slightly faster.
    """
    flags = []
    if os.path.islink(path):
        # This is *not* going to show the identical linked path as
        # (for instance) 'ls' or 'tree', but it should be simply
        # comparable to another DirTree link
        flags.append('@')
        far = os.path.realpath(path)
        head, tail = os.path.split(path)
        rel = os.path.relpath(far, head)
        flags.append(' -> %s'%rel)
        if os.path.isdir(far):
            flags.append('/')
            # We don't try to cope with a "far" executable, or if it's
            # another link (does it work like that?)
    elif os.path.isdir(path):
        flags.append('/')
        if fold_dirs and filename in fold_dirs:
            flags.append('...')
    else:
        s = os.stat(path)
        m = s.st_mode
        if (m & stat.S_IXUSR) or (m & stat.S_IXGRP) or (m & stat.S_IXOTH):
            flags.append('*')
    return '%s%s'%(filename, ''.join(flags))

if False:
    T = '+-'
    L = '+-'
    B = '| '
    S = '  '
else:
    T = '├─'
    L = '└─'
    B = '│ '
    S = '  '

def tree(dirpath, padding='', fold_dirs=None):
    filenames = sorted(os.listdir(dirpath))
    for count, name in enumerate(filenames):
        path = os.path.join(dirpath, name)
        if os.path.isdir(path):
            if count+1 == len(filenames):
                new_padding = padding + L
            else:
                new_padding = padding + T
            print new_padding + filestr(path, name, fold_dirs)

            if fold_dirs and name in fold_dirs:
                continue

            if count+1 == len(filenames):
                new_padding = padding + S
            else:
                new_padding = padding + B
            tree(path, new_padding, fold_dirs=fold_dirs)
        else:
            if count+1 == len(filenames):
                new_padding = padding + L
            else:
                new_padding = padding + T
            print new_padding + filestr(path, name, fold_dirs)

def main(args):

    where = None
    fold_dirs = []

    while args:
        word = args.pop(0)
        if word in ('-h', '-help', '--help'):
            print __doc__
            return
        elif word == '-s':
            fold_dirs.append(args.pop(0))
        elif where is None:
            where = word
        else:
            print 'Unexpected command line argument %r'%word

    if where is None:
        where = '.'

    path = os.path.abspath(where)
    print filestr(path, os.path.basename(path))
    tree(path, fold_dirs=fold_dirs)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)

# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
