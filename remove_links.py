#! /usr/bin/env python

"""remove_links.py -- remove/delete soft links in this directory and its
subdirectories.
"""

import os

for dirpath,dirname,filenames in os.walk('.'):
  print 'Directory',dirpath
  for name in filenames:
    path = os.path.join(dirpath,name)
    if os.path.islink(path):
      print 'Removing link',path
      os.remove(path)
