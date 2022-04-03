#! /usr/bin/env python3

"""Usage: circ.py [draw] [ref] <circumference> [<circumference> ...] [inches]
          circ.py [draw] [ref] diam <diameter> [<diameter> ...] [inches]

How *does* one draw a circle of a realistic size on the monitor?

Without counting pixels...

Given a circle's circumference, print out its diameter.
(With 'diam') given a circle's diameter, print out its circumference.

Several values can be given - for instance:

  circ.py 2 3.5 4
  circ.py diam 2.6 3.9

With 'diam', the value is assumed to be a circle's diameter, and the
circumference is printed out instead. The 'diam' may be anywhere on the command
line, but affects the meaning of all values.

If the word 'draw' is given, then a temporary PDF file showing the circle(s)
will be created and opened (with Preview or whatever else has been set as
the standard way of opening PDFfiles). The word 'draw' can be given anywhere.

If the word 'ref' is given, a 5cm diameter reference circle will be drawn
in red.

Both <circumference> and <diameter> default to centimetres, unless they end
with 'in', in which case that value is in inches. So:

  circ.py draw 3 5in

draws circumferences of 3 centimetres and 5 inches (although all values will
still be reported in centimetres). For symetry, values can (redundantly) end
in 'cm' to mean centimetres. Thus ending in 'mm' inevitably means millimetres...
"""

# Installation (for instance):
#
# - makevirtualenv -p $(which python3) py3
# - pip install reportlab

import os
import sys
import time

from math import pi
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import subprocess

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import cm

@contextmanager
def temporary_circle_file():
    f = NamedTemporaryFile(delete=False, suffix='.pdf')
    yield f
    os.remove(f.name)

def normalise_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    path = os.path.normpath(path)   # remove double slashes, etc.
    return path

def draw(diameters, filename='circle.pdf', ref=None):
    """Draw a circle of each value from 'diameters' cm in file 'filename'

    If 'ref' is given, it should be the diameter of a "reference" circle,
    which will be draw in red.
    """
    print('Writing to file {}'.format(filename))

    max_diameter = max(diameters)
    if ref:
        max_diameter = max(max_diameter, ref)

    min_dimension = 5 * cm
    ask_dimension = max_diameter * cm * 2
    use_dimension = ask_dimension if ask_dimension > min_dimension else min_dimension
    pagesize = (use_dimension, use_dimension)

    pdf = Canvas(filename, pagesize=pagesize)

    xpos = ypos = use_dimension / 2

    for diameter in diameters:
        radius = diameter / 2.0
        pdf.circle(xpos, ypos, radius * cm)

    pdf.setFont('Courier', 10)
    text = pdf.beginText(10, 20)    # origin is in the bottom left
    diams = []
    circs = []
    for diameter in diameters:
        diams.append('{:.3}'.format(diameter))
        circs.append('{:.3}'.format(diameter*pi))
    text.textLine('d {}cm'.format(','.join(diams)))
    text.textLine('C {}cm'.format(','.join(circs)))
    pdf.drawText(text)

    if ref:
        pdf.setStrokeColorRGB(1.0, 0.0, 0.0)
        radius = ref / 2.0
        pdf.circle(xpos, ypos, radius * cm)

    pdf.showPage()
    pdf.save()

def main(args):
    REF_DIAMETER = 5.0
    ref = None
    values = []
    is_circumference = True
    draw_it = False
    while args:
        word = args.pop(0)
        if word in ('-h', '-help', '--help', 'help'):
            print(__doc__)
            return 0
        elif word == 'draw':
            draw_it = True
        elif word == 'diam':
            is_circumference = False
        elif word == 'ref':
            ref = REF_DIAMETER
        else:
            is_mm = False
            is_inches = False
            if word.endswith('cm'):
                word = word[:-2]
            elif word.endswith('mm'):
                is_mm = True
                word = word[:-2]
            elif word.endswith('in'):
                is_inches = True
                word = word[:-2]
            try:
                value = float(word)
            except ValueError as e:
                print('{0!r} is not a floating point {1}'.format(word,
                    'circumference' if is_circumference else 'diameter'))
                print(e)
                return 1
            if is_inches:
                # Since July 1959, an inch has been defined as 25.4mm
                value = value * 2.54
            elif is_mm:
                value = value / 10
            values.append(value)

    if not values:
        print(__doc__)
        return 1

    try:
        values = [float(value) for value in values]
    except ValueError as e:
        print(e)
        return 1

    values = sorted(set(values))

    if is_circumference:
        diameters = [value/pi for value in values]
        for value in values:
            diameter = value/pi
            circumference = value
            print('Circumference {0}cm -> diameter {1:.3}cm'.format(circumference, diameter))
    else:
        diameters = values
        for value in values:
            diameter = value
            circumference = value*pi
            print('Diameter {0}cm -> circumference {1:.3}cm'.format(diameter, circumference))

    if draw_it:
        with temporary_circle_file() as f:
            draw(diameters, f.name, ref=ref)
            retcode = subprocess.call(['open', f.name])
            # And rather crudely, give it a little time to finish opening
            # (otherwise sometimes 'open' won't find the file still there)
            time.sleep(0.4)
            return retcode


if __name__ == '__main__':
    args = sys.argv[1:]
    retcode = main(args)
    sys.exit(retcode)
