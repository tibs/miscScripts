#! /usr/bin/env python3

"""Usage: tree.py [-f[old] <dir>] [-a[scii]] [<directory>]

Directories named by '-fold' ('-f') will not have their content shown
You may nominate multiple "folded" directories, but each needs to be
preceded by the switch. For instance::

    tree.py -f .git -f .weld fromble

(but actually .git directories are currently always folded - this is a hack)

If you specify '-ascii' ('-a') then "normal" characters will be used to show
the tree structure, instead of IBM437 characters (this is similar to the "real"
tree's '--charset=ASCII')

If you specify -d then only directories will be shown.

__pycache__ directories are not shown (this is a hack)
"""

# TODO: ignore __pycache__ directories by default
#           -ignore <dir>       -- defaults to -ignore __pycache__
#           -noignore <dir>     -- use -noignore __pycache__ to see them
# TODO: fold .git directories by default - so need to rethink how folding works
#           -fold <dir>         -- defaults to -fold .git
#           -nofold <dir>       -- use -nofold .git to see their content
# TODO: use Python3 facilities instead of older Python2 mechanisms
# TODO: use argparse because the command line is now getting complicated,
#       and also because it should allow -f to take a *list* of names,
#       as well as allowing it to be specified more than once.

import sys
import os
import stat

INDENT = '    '

DEFAULT_IGNORE = ['__pycache__']


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
        flags.append(' -> %s' % rel)
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
    return '%s%s' % (filename, ''.join(flags))


def tree(dirpath, padding='', fold_dirs=None, just_ascii=False, only_dirs=False):

    if just_ascii:
        if True:            # Follow how Unix 'tree' does it
            T = '|- '
            L = '`- '
            B = '|  '
            S = '   '
        else:               # A heavier-weight alternative
            T = '+-'
            L = '+-'
            B = '| '
            S = '  '
    else:
        T = '├─'
        L = '└─'
        B = '│ '
        S = '  '

    filenames = sorted(os.listdir(dirpath))
    for count, name in enumerate(filenames):
        path = os.path.join(dirpath, name)
        if os.path.isdir(path):

            # TODO Really, we should have this switchable
            if name in DEFAULT_IGNORE:
                continue

            if count+1 == len(filenames):
                new_padding = padding + L
            else:
                new_padding = padding + T
            print(new_padding + filestr(path, name, fold_dirs))

            if fold_dirs and name in fold_dirs:
                continue

            if count+1 == len(filenames):
                new_padding = padding + S
            else:
                new_padding = padding + B
            tree(path, new_padding, fold_dirs=fold_dirs, just_ascii=just_ascii, only_dirs=only_dirs)
        elif only_dirs:
            continue
        else:
            if count+1 == len(filenames):
                new_padding = padding + L
            else:
                new_padding = padding + T
            print(new_padding + filestr(path, name, fold_dirs))


def main(args):

    where = None
    just_ascii = False
    fold_dirs = []
    only_dirs = False

    while args:
        word = args.pop(0)
        if word in ('-h', '-help', '--help'):
            print(__doc__)
            return
        elif word in ('-f', '-fold'):
            fold_dirs.append(args.pop(0))
        elif word in ('-a', '-ascii'):
            just_ascii = True
        elif word == '-d':
            only_dirs = True
        elif where is None:
            where = word
        else:
            print('Unexpected command line argument %r' % word)

    if where is None:
        where = '.'

    # TODO This is a hack - it should be optional
    if '.git' not in fold_dirs:
        fold_dirs.append('.git')

    path = os.path.abspath(where)
    print(filestr(path, os.path.basename(path)))
    tree(path, fold_dirs=fold_dirs, just_ascii=just_ascii, only_dirs=only_dirs)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
