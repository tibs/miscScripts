#!/usr/bin/env python

"""Show what programs are on the path, sorted alphabetically.

Usage: %s [ <switches> ] [ <regexp> ]

    Where:
        -verbose        list directories being queried, etc. 

        -help           prints out this text
        -version        prints out the version information
	-history        prints out the history information

 If no <regexp> is given, all executables on the path are reported.

 The <regexp> is interpreted as a Python 're' regular expression, similar to
 those which available in Perl and, to some extent, egrep. Matching is done
 with re.search. For instance:

        onpath '.*te.*'

 will find all executables on the path which have the letter sequence "te"
 anywhere in their name.

        onpath gothic

 will find all executables on the path that contain "gothic".

 NOTE that on Unix one must also remember aliases, and on NT doskey macros...
"""

__version__ = "1.2 (Tibs)"
__history__ = """\
1998-??-??: Created by Tibs
1999-11-05: Now works on Unix and NT
2006-10-06: Converted from regexp to re, and improved link handling
"""

import sys
import os
import string
import stat
import re

if os.name == "nt":
    PATH_DELIM = ";"
else:
    PATH_DELIM = ":"


# ------------------------------------------------------------
def environ(item,verbose=0):
    """Try to cope with case differences in environment variables..."""

    if os.environ.has_key(item):
        if verbose: print "Trying %s"%item
        return os.environ[item]
    else:
        other = []
        up = string.upper(item)
        if up != item: other.append(up)
        down = string.lower(item)
        if down != item: other.append(down)
        cap = string.upper(item[0]) + string.lower(item[1:])
        if cap != item: other.append(cap)

        for name in other:
            if verbose: print "Trying %s"%name
            if os.environ.has_key(name):
                return os.environ[name]

        raise KeyError,\
              "There is no environment variable %s (also tried %s)"%\
              (item,string.join(other,", "))


# ------------------------------------------------------------
def get_tuple(file):
    """Return a tuple of (filename,indirection,directory) for "file".

    "filename"    is the file name component of "file".
    "indirection" is either "@" (if the file is a link) or " ".
    "directory"   is the directory component of "file".

    Returns None if it can't work things out.
    """

    # Ignore directories

    if os.path.isdir(file):
	return None

    # If it is a link, chase down the mode of the file at the other end
    # (multiple links get taken care of automatically)

    if os.name == "posix":
    	if os.path.islink(file):
            at   = "@"
            link = os.readlink(file)
            # Allow for a link that is *not* an absolute path
            dir,name = os.path.split(file)
            link = os.path.join(dir,link)
            link = os.path.normpath(link)
	else:
            at = " "	# it's not a link
            link = file
        try:
            mode = os.lstat(link)[stat.ST_MODE]
        except:
            return None	# ignore awkward cases

    	# Ignore things which don't have the "x" bit set
	if not mode & 00111:
		return None
    else:
    	at = " "	# it can't be a link

    # Otherwise, return the appropriate tuple

    dir, thing = os.path.split(file)

    return (thing,at,dir)



# ------------------------------------------------------------
def onpath(pattern_string,verbose=0):

    if pattern_string:
        print 'Looking for stuff matching %s'%(`pattern_string`)
        pattern = re.compile(pattern_string)
    else:
	print 'Looking for all executables'
        pattern = None

    # Get the path as a string
    try:
        path_string = environ("PATH",verbose)
    except KeyError,what:
        print what
        return

    # Split it into a list of directories
    path = string.splitfields(path_string,PATH_DELIM)

    # Find all the files in those directories
    # - construct a list of tuples of the form (file, at, directory)
    #   (where "at" is "@" for a link, " " for other files)
    # - use a dictionary so that we don't get duplicate entries

    files = {}
    tuples = {}

    for dir in path:
        if os.name == "nt" and dir == "":
            # On NT, we sometimes get an empty string as a directory
            # - interpret it as the current directory?
            dir = os.curdir
        elif dir != "." and dir != "..":
            # Allow for directories relative to the current directory
            # (we don't try "." and ".." because they give strange
            #  results with os.path.join used as follows!)
            dir = os.path.join(os.curdir,dir)

        if os.path.exists(dir):
            if verbose: print 'Looking in   "%s"'%dir
	    list = os.listdir(dir)
        else:
            if verbose: print 'No directory "%s"'%dir
            continue

	for thing in list:
	    if pattern != None:
                ##
                ##if dir == "/usr/bin" and "gcc" in thing:
                ##    print "Checking '%s'"%thing
                ##
		if pattern.search(thing) is None:
		    continue
                ##
                ##elif dir == "/usr/bin" and "gcc" in thing:
                ##    print "...found",pattern_string
                ##

	    file = os.path.join(dir,thing)

	    tuple = get_tuple(file)
            ##
            ##if dir == "/usr/bin" and "gcc" in thing:
            ##    print "...tuple",tuple
            ##

	    if tuple == None:
		continue
	    else:
                # For each filename, we record a list of where it has
                # been located...
                filename,indirect,directory = tuple
                location = (indirect,directory)
                if files.has_key(filename):
                    if location not in files[filename]:
                        files[filename].append(location)
                else:
                    files[filename] = [location]

    # Sort them by file (program) name
    names = files.keys()
    names.sort()

    # And print them out
    if len(names) == 0:
	print "  Nothing found"
    else:
        maxlen = 0
        for name in names:
            if len(name) > maxlen:
                #print "Length %2d: %s"%(len(name),name)
                maxlen = len(name)
        format1 = " %-" + "%d"%(maxlen+2) + 's in %1s "%s"'
        format2 = " "   + " " *(maxlen+2) +  '    %1s "%s"'
	for name in names:
            locns = files[name]
            first = 1
            for at,dir in locns:
                if first:
                    print format1%(name,at,dir)
                    first = 0
                else:
                    print format2%(at,dir)


# ------------------------------------------------------------
def print_usage(argv0):
    script_name = string.split(argv0, os.sep)[-1]
    print __doc__%(script_name)

def main():
    """Do it."""

    # Extract our arguments

    arg_list = sys.argv[1:]

    # What arguments do we have?

    if len(arg_list) == 0:
        onpath(None,verbose=0)
    elif len(arg_list) == 1:
        if arg_list[0] == "-help":
            print_usage(sys.argv[0])
        elif arg_list[0] == "-version":
            print "Version:",__version__
        elif arg_list[0] == "-history":
            print "History:"
            print __history__
        elif arg_list[0] == "-verbose":
            onpath(None,verbose=1)
        else:
            onpath(arg_list[0],verbose=0)
    elif len(arg_list) == 2 and arg_list[0] == "-verbose":
        onpath(arg_list[1],verbose=1)
    else:
        print_usage(sys.argv[0])

# If we're run from the shell, run ourselves
if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# vim: set filetype=python expandtab shiftwidth=4:
# [X]Emacs local variables declaration - place us into python mode
# Local Variables:
# mode:python
# py-indent-offset:4
# End:
