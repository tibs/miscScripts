#! /usr/bin/env python3

"""Extract the contents of an RPM.

Assumes you have rpm2cpio and cpio installed.

Usage:

    unrpm.py <rpm-filename>.rpm

Creates a directory called <rpm-filename>, and extracts the content of the
RPM therein
"""

import os
import sys
import subprocess

def main(args):
    if len(args) != 1 or args[0] in ('-h', '-help', '--help'):
        print(__doc__)
        return

    filepath = os.path.abspath(args[0])
    print(filepath)
    base, ext = os.path.splitext(filepath)

    os.mkdir(base)
    os.chdir(base)

    rpm2cpio = subprocess.Popen(['rpm2cpio', filepath], stdout=subprocess.PIPE)
    subprocess.check_call(['cpio', '-idmv'], stdin=rpm2cpio.stdout)


if __name__ == '__main__':
    main(sys.argv[1:])
