Useful scripts
==============
A collection of scripts of varying utility.

Note: these are mostly very old. That means some of them don't even try to
follow PEP 8. Minimal changes have been made to allow them to work with
Python 3.

``__linkup.py`` Run this to make links from ``${HOME}/bin`` to all the scripts
in this directory. The links omit the extension, which works well on Unices.
``-h`` for help.

``change_extension.py`` An old script which does what it says.  ``-h`` for
help.

``check_indent.py`` Reports on the indentation in a file. Not sure why I wrote
it.  No help. Read its docstring.

``circ.py`` Back in the day, I remember measuring the pixels on early colour
raster displays, so we could work out their size and aspect ration (different
from display to display) and draw accurate circles. Nowadays, I thought,
surely it must be simpler to draw a circle of a particular size on a screen.
As it turned out, somewhat harder than I expected, and the easiest thing to do
was to use the ``reportlab`` package, which works all that out for me. I was
a bit disappointed, but here is a program that draws circles of the requested
size, and for fun, will also convert circumference to diameter. It's also
possible to draw a reference circle (5cm diameter for no good reason - 10cm
seemed a bit big). I'm afraid there's no packaging of this - you need to
install ``reportlab`` by hand.

``editpath.py`` Edit a PATH string, and return the result.  ``-h`` for help.
Less useful now I use the fish_ shell, which has commands to do this sort of
thing.

.. _fish: https://fishshell.com/

``friday.py`` Give the date of a Friday.  ``-h`` for help. This was once
useful when I had to keep timesheets.

``html2text.py`` A newer attempt at a general "thing" to text converter
(replacing the *very old* version that was here before). It uses ``antiword``
or ``pandoc`` to convert various formats. I wrote this and then don't seem to
have used it much. ``-h`` for help.

``mb.py`` This was written on VMS, where it was useful. Report on file sizes,
and/or convert bytes to/from megabytes.  ``-h`` for help.

``natgrid.py`` Once upon a time I did work with OS(GB) maps. This script
converts to/from National Grid references.  No help. Read its docstring.

``unrpm.py`` Runs ``rmp2cpio`` and ``cpio`` to extract the contents from an
RPM file (who'd have thought the RPM command didn't support that!). ``-h`` for
help. No idea if this is still useful.

``remove_twiddle_files.py`` Find and delete files ending with "~", and other
files of the sort that get left lying around (with an option to remove
``.pyc`` files as well).  ``-h`` for help.

``rundoctest.py`` A simple script to run doctest.py over a file.  ``-h`` for
help.

``setup_muddle.py`` I used to source this in my '.bashrc' file to set up my
usage of muddle_. So it may be of no interest to anyone else.

.. _muddle: https://github.com/kynesim/muddle

``showpath.py`` Show the PATH, or the PYTHONPATH, or various other paths, in a
useful manner, reporting on duplicates. Works on Windows as well.  ``-h`` for
help.

``tidypath.py`` Return a new string representing a PATH without duplicates.
``-h`` for help.
Less useful now I use the fish_ shell, which has commands to do this sort of
thing.

``tree.py`` A very simple version of the Linux "tree" utility, written to
allow me to "fold" directories whose content is not of interest. So ``tree.py
-f .git`` will show a ``.git`` directory as present, but not show its
contents. The ``-a`` switch is useful to output a simple ASCII version of the
tree structure. Again, ``-h`` for help.
