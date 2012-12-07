#!/usr/bin/env python

"""Simple utility to make some attempt at turning HTML into text

	usage: html2text [<switches>] htmlfile
	       html2text [<switches>] -all [directory [directory ...]]
	       html2text -auto [directory [directory ...]]

Switches:
   -all      all ".html", ".shtml" and ".htm" files in the named directory or
             directories (default ".") will be processed.
   -verbose  each file is named as it is processed.
   -force    the output file will overwrite any existing file of that name.
   -delete   the HTML file will be deleted if it is successfully translated.
   -auto     the same as "-all -verbose -delete".
   -compress, -gzip, -z   compress the result with gzip
   -recurse,  -r          recurse through directories, implies -all

NB: .doc and .rtf files are also converted, but will not be deleted.
"""

import sys
import os
import string
import htmllib
import formatter


def deduce_filename(htmlfile):
    """Deduce a text filename from an HTML filename."""

    #head,tail = os.path.splitext(htmlfile)
    #
    #if tail == ".html" or tail == ".htm":
    #    return head+".txt"
    #else:
    #    return htmlfile+".txt"
    return htmlfile+".txt"


class MyHTMLParser(htmllib.HTMLParser):

    def __init__(self, formatter, verbose=0):
	htmllib.HTMLParser.__init__(self, formatter, verbose)

    def anchor_bgn(self, href, name, type):
        self.anchor = href
        if self.anchor:
	    self.save_bgn()

    def anchor_end(self):
        if self.anchor:
	    text = self.save_end()
	    self.handle_data("%s <%s>"%(text,self.anchor))
	    self.anchor = None


DEBUG = 0

class MyWriter(formatter.NullWriter):

    def __init__(self, file=None, maxcol=72):
	self.file = file or sys.stdout
	self.maxcol = maxcol
	self.margin = 0		# margin
	self.extra_margin = 0	# extra margin in a list element
	self.indent = 3		# increment for margin
	self.extra_indent = 2	# indent for extra margin
	self.level = {}		# dictionary of levels
	formatter.NullWriter.__init__(self)
	self.reset()

    def reset(self):
	self.col = 0		# current column
	self.atbreak = 0	# is this a good place to linebreak?

    def new_alignment(self, align):
	if DEBUG: print "new_alignment(%s)" % `align`

    def new_font(self, font):
	if DEBUG: print "new_font(%s)" % `font`

    def new_margin(self, margin, level):
	if DEBUG: print "new_margin(%s, %d)" % (`margin`, level)

	if margin == None:
	    self.margin = 0
	elif self.level.has_key(margin):
	    if level == 1:
		self.level[margin] = level
		self.margin = self.margin + self.indent
	    elif level == 2:
		self.level[margin] = level
		self.margin = self.margin - self.indent
		if self.margin < 0: self.margin = 0
	else:
	    self.level[margin] = level
	    self.margin = self.margin + self.indent
	if DEBUG: print "   margin =",self.margin
	self.extra_margin = 0
	return


	if margin == None:
	    self.margin = 0
	elif level == 1:
	    self.margin = self.margin + self.indent
	elif level == 2:
	    self.margin = self.margin - self.indent
	    if self.margin < 0: self.margin = 0
	else:
	    print "***Margin %s level %d (not 1 or 2)"%(margin,level)
	    self.margin = 0
	if DEBUG: print "   margin =",self.margin
	self.extra_margin = 0
	#self.reset()  #???
	#self.start_margin()

    def new_spacing(self, spacing):
	if DEBUG: print "new_spacing(%s)" % `spacing`

    def new_styles(self, styles):
	if DEBUG: print "new_styles(%s)" % `styles`

    def send_paragraph(self, blankline):
	if DEBUG: print "send_paragraph(%s)" % `blankline`
	if blankline > 1:
	    self.file.write('\n'*(blankline-1))
	self.reset()
	self.file.write("\n")
	##self.start_line()

    def send_line_break(self):
	if DEBUG: print "send_line_break()"
	#self.file.write('\n')
	self.reset()
	self.file.write("\n")
	##self.start_line()

    def send_hor_rule(self, *args, **kw):
	if DEBUG: print "send_hor_rule(%s,%s)"%(args,kw)
	self.file.write('\n')
	self.file.write('-'*self.maxcol)
	self.file.write('\n')
	self.reset()

    def start_margin(self):
	if DEBUG: print "   start_margin()"
	self.file.write(" "*self.margin + " "*self.extra_margin)
	self.col = self.col + self.margin

    def start_line(self):
	if DEBUG: print "   start_line()"
	self.file.write("\n")
	self.start_margin()
	#self.file.write("\n" + " "*self.margin + " "*self.extra_margin)
	#self.col = self.col + self.margin

    def send_label_data(self, data):
	if DEBUG: print "send_label_data(%s)" % `data`
	self.extra_margin = 0
	self.start_line()
	self.file.write(data+" ")
	self.extra_margin = self.extra_indent

    def send_flowing_data(self, data):
	if DEBUG: print "send_flowing_data(%s)" % `data`
	if not data: return
	atbreak = self.atbreak or data[0] in string.whitespace
	col = self.col

	if col == 0:
	    self.start_margin()

	maxcol = self.maxcol
	write = self.file.write
	#self.start_line()
	for word in string.split(data):
	    if atbreak:
		if col + len(word) >= maxcol:
		    #write('\n')
		    col = 0
		    self.start_line()
		else:
		    write(' ')
		    col = col + 1
	    write(word)
	    if DEBUG: print "   ",word
	    col = col + len(word)
	    atbreak = 1
	self.col = col
	self.atbreak = data[-1] in string.whitespace

    def send_literal_data(self, data):
	if DEBUG: print "send_literal_data(%s)" % `data`
	self.file.write(data)
	i = string.rfind(data, '\n')
	if i >= 0:
	    self.col = 0
	    data = data[i+1:]
	data = string.expandtabs(data)
	self.col = self.col + len(data)
	self.atbreak = 0


def textutil(docfile,textfile,force=0,verbose=0,problems=None,
             delete=0,compress=0):
    """Do the conversion."""

    if os.path.exists(textfile) and not force:
	print "Can't write %s - it already exists"%textfile
	return

    if verbose:
	print "%-40s:"%docfile,

    err = os.system("textutil -convert txt -output '%s' '%s'"%(textfile,docfile))

    if compress:
	if verbose: print "Compressing.. ",
        if force:
            os.system("gzip -f '%s'"%textfile)
        else:
            os.system("gzip '%s'"%textfile)

    if verbose: print



def antiword(docfile,textfile,force=0,verbose=0,problems=None,
             delete=0,compress=0):
    """Do the conversion."""

    if os.path.exists(textfile) and not force:
	print "Can't write %s - it already exists"%textfile
	return

    if verbose:
	print "%-40s:"%docfile,

    err = os.system("antiword -f '%s' > '%s'"%(docfile,textfile))

    if compress:
	if verbose: print "Compressing.. ",
        if force:
            os.system("gzip -f '%s'"%textfile)
        else:
            os.system("gzip '%s'"%textfile)

    if verbose: print



def convert(htmlfile,textfile,force=0,verbose=0,problems=None,
            delete=0,compress=0):
    """Do the conversion."""

    if os.path.exists(textfile) and not force:
	print "Can't write %s - it already exists"%textfile
	return

    if verbose:
	print "%-40s:"%htmlfile,

    ff = open(htmlfile,"r")
    data = ff.read()
    ff.close()

    if verbose:
	print "Writing.. ",

    ww = open(textfile,"w")
    fmtr = formatter.AbstractFormatter(MyWriter(ww))

    p = MyHTMLParser(fmtr)
    try:
        try:
            p.feed(data)
        finally:
            ww.close()
            p.close()
        if delete:
            if verbose:
                print "Deleting.. ",
            os.remove(htmlfile)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
	if verbose: print
        print "Exception processing %s - %s: %s"%(textfile,sys.exc_type,
                                                  sys.exc_value)
        if problems != None:
            problems.append(htmlfile)
        if os.path.exists(textfile):
            os.remove(textfile)

        print "Trying textutil instead"
        os.system("textutil -convert txt -output '%s' '%s'"%(textfile,htmlfile))

    if compress:
	if verbose: print "Compressing.. ",
        if force:
            os.system("gzip -f '%s'"%textfile)
        else:
            os.system("gzip '%s'"%textfile)

    if verbose: print

def unquotify(directory,file):
    if "'" in file:
        print "Removing single quotes from file %s"%os.path.join(directory,file)
        newfile = ""
        # Ick -- don't do it this way!
        for letter in file:
            if letter == "'":
                newfile += "_"
            else:
                newfile += letter
        os.rename(os.path.join(directory,file),
                  os.path.join(directory,newfile))
        file = newfile
    return file

def convert_file(directory,file,force=0,verbose=0,problems=None,delete=0,recurse=0,compress=0):

    name,ext = os.path.splitext(file)
    ext = string.lower(ext)
    if ext in (".html", ".shtml", ".htm"):
        file = unquotify(directory,file)
        textfile = deduce_filename(file)
        convert(os.path.join(directory,file),
                os.path.join(directory,textfile),force=force,
                verbose=verbose,problems=problems,delete=delete,compress=compress)
    elif ext == ".doc":
        file = unquotify(directory,file)
        textfile = file + ".txt"
        antiword(os.path.join(directory,file),
                 os.path.join(directory,textfile),force=force,
                 verbose=verbose,problems=problems,delete=delete,compress=compress)
    elif ext == ".rtf":
        file = unquotify(directory,file)
        textfile = file + ".txt"
        textutil(os.path.join(directory,file),
                 os.path.join(directory,textfile),force=force,
                 verbose=verbose,problems=problems,delete=delete,compress=compress)


def process_dir(directory,force=0,verbose=0,problems=None,delete=0,recurse=0,compress=0):
    if not verbose: print "Directory",directory
    files = os.listdir(directory)
    files.sort()
    for file in files:
	path = os.path.join(directory,file)
	if os.path.isdir(path):
	    if recurse:
		process_dir(path,force=force,verbose=verbose,problems=problems,
				delete=delete,recurse=recurse,compress=compress)
	else:
            convert_file(directory,file,
                         force=force,verbose=verbose,problems=problems,
                         delete=delete,recurse=recurse,compress=compress)



def main():
    """Do it."""

    all   = 0
    force = 0
    debug = 0
    verbose = 0
    delete = 0
    recurse = 0
    compress = 0
    args  = []

    # What arguments do we have?

    arg_list  = sys.argv[1:]

    while 1:
	if len(arg_list) == 0:
	    break

	word = arg_list[0]

	if word == "-help" or word == "-h":
	    print __doc__
	    return
	elif word == "-debug":		# undocumented command
	    debug = 1
	elif word == "-force":
	    force = 1
        elif word in ("-recurse","-r"):
	    recurse = 1
	    all = 1
        elif word in ("-compress", "-gzip", "-z"):
	    compress = 1
	elif word == "-verbose":
	    verbose = 1
	elif word == "-delete":
	    delete = 1
	elif word == "-all":
	    all = 1
	elif word == "-auto":
	    all = 1
	    delete = 1
	    verbose = 1
	else:
	    args.append(word)

	arg_list = arg_list[1:]
	continue

    if debug:
	global DEBUG
	DEBUG = 1

    if all:
        problems=[]
	if len(args) == 0:
	    args.append(".")
	for dir in args:
	    if not os.path.isdir(dir): continue
            process_dir(dir,force=force,verbose=verbose,problems=problems,delete=delete,recurse=recurse,
			    compress=compress)
        if problems:
            print "Problems were encountered with:"
            for name in problems:
                print "  ",name
    else:
	if len(args) == 1:
            directory,file = os.path.split(args[0])
            convert_file(directory,file,
                         force=force,verbose=verbose,problems=problems,
                         delete=delete,recurse=recurse,compress=compress)
	else:
	    print __doc__
	    return

# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# [X]Emacs local variables declaration - place us into python mode
# Local Variables:
# mode:python
# py-indent-offset:4
# End:
