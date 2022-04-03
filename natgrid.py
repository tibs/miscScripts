#!/usr/bin/env python3

"""Convert from/to an OS(GB) National Grid reference.

Usage: natgrid <grid reference>

       Returns the location of the bottom left (SW) corner of the relevant
       square (in metres east and north of the OS(GB) false origin), along
       with its size and its putative grid interval.

       <grid reference> is in one of the following forms:
             TQ
             TQ 3 7
             TQ 38 77
             TQ 389 770
             TQ 3893 7706

       Note that leading zeroes must be provided in the numeric fields
       where needed to indicate the precision.

   or: natgrid <east> <north>

       Returns the National Grid reference of the given location,
       where <east> and <north> are easting and northing respectively.
"""

__version__ = "1.0 1997-07-16"
__history__ = """History

1996-06-27 - Created by Tony J Ibbs <tibbs@geog.gla.ac.uk>
1997-07-16 - Tony J Ibbs
             Add ability to go from coordinate to national grid reference.

And then amended for Python3, 2022-04-03
"""

# Testing:
# According to JB Harley, "Ordnance Survey Maps: a descriptive manual"
# (which is my source), we have the following correspondences:
#
# Point at 538,932 E  177,061 N has the grid references:
#
#        TQ 38   77        scale 1:250000 (etc)  grid: 10000m  precision: 1000m
#        TQ 389  770        scale 1:50000  (etc)  grid:  1000m  precision:  100m
#        TQ 3893 7706        scale 1:2500   (etc)  grid:   100m  precision:   10m

import sys
import string
import os


# ----------------------------------------------------------------------
# Dictionaries convert the letter into (easting,northing) tuples (i.e., x,y),
# Units are kilometres

ref100 = {"S":(0,   0),"T":(500,   0),
          "N":(0, 500),"O":(500, 500),
          "H":(0,1000),"J":(500,1000)}

ref10 = {"A":(0,400),"B":(100,400),"C":(200,400),"D":(300,400),"E":(400,400),
         "F":(0,300),"G":(100,300),"H":(200,300),"J":(300,300),"K":(400,300),
         "L":(0,200),"M":(100,200),"N":(200,200),"O":(300,200),"P":(400,200),
         "Q":(0,100),"R":(100,100),"S":(200,100),"T":(300,100),"U":(400,100),
         "V":(0,  0),"W":(100,  0),"X":(200,  0),"Y":(300,  0),"Z":(400,  0)}

def from_ref(arg_list):
    """Convert a national grid refernce to location, etc.

    arg_list -- contains either one or three values, for our grid reference.
    """

    arg_len = len(arg_list)

    # Check the values given make sense

    prefix = arg_list[0].upper()

    if len(prefix) != 2:
        print("Grid reference %s does not make sense"%arg_list.join())
        print("The first part of a grid reference must be two characters")
        return

    if arg_len == 3:
        Estr = arg_list[1]
        Nstr = arg_list[2]

        if len(Estr) != len(Nstr):
            print("Grid reference %s does not make sense"%arg_list.join())
            print("The easting and northing must be of the same size.")
            return

    # Extract the two letters at the start, which determine which 100km
    # square the location is in

    try:
        bigx,bigy = ref100[prefix[0]]                # 100 km square
        litx,lity = ref10 [prefix[1]]                #  10 km square
    except:
        print("Grid reference %s does not make sense"%arg_list.join())
        print("The first letter must be H,J,N,O,S or T, and the second must " \
              "be A-H or J-Z")
        return

    xloc = (bigx + litx) * 1000                # in metres
    yloc = (bigy + lity) * 1000

    # Now deal with any numeric portion

    if arg_len == 3:
        if len(Estr) == 1:
            print("Scale:         not defined")
            print("Grid interval: 100,000 metres")
            precision = 10000
        elif len(Estr) == 2:
            print("Scale:         1:625,000 or 1:250,000")
            print("Grid interval: 10,000 metres")
            precision = 1000
        elif len(Estr) == 3:
            print("Scale:         1:63,360, 1:50,000, 1:25,000, 1:10,000  " \
                  "or 1:10,560")
            print("Grid interval: 1,000 metres")
            precision = 100
        elif len(Estr) == 4:
            print("Scale:         1:2500 or 1:1250")
            print("Grid interval: 100 metres")
            precision = 10
        else:
            print("Grid reference %s does not make sense"%arg_list.join())
            print("The numbers must each be 1 to 4 digits long.")
            return

        try:
            easting  = int(Estr,10)
        except:
            print("Grid reference %s does not make sense"%arg_list.join())
            print("%s is not a number"%Estr)
            return

        try:
            northing = int(Nstr,10)
        except:
            print("Grid reference %s does not make sense"%arg_list.join())
            print("%s is not a number"%Nstr)
            return

        xloc = xloc + (easting  * precision)
        yloc = yloc + (northing * precision)
    else:
        print("Scale:         not defined")
        print("Grid interval: 100,000 metres (notionally)")

    # And we can report the actual location...

    print("Easting:       %d"%xloc)
    print("Northing:      %d"%yloc)



# ----------------------------------------------------------------------
# Dictionaries convert the (easting,northing) tuples (i.e., x,y) into
# letters. Units are kilometres.

tup100 = {(0,   0):"S",(500,   0):"T",
          (0, 500):"N",(500, 500):"O",
          (0,1000):"H",(500,1000):"J"}

tup10 = {(0,400):"A",(100,400):"B",(200,400):"C",(300,400):"D",(400,400):"E",
         (0,300):"F",(100,300):"G",(200,300):"H",(300,300):"J",(400,300):"K",
         (0,200):"L",(100,200):"M",(200,200):"N",(300,200):"O",(400,200):"P",
         (0,100):"Q",(100,100):"R",(200,100):"S",(300,100):"T",(400,100):"U",
         (0,  0):"V",(100,  0):"W",(200,  0):"X",(300,  0):"Y",(400,  0):"Z"}

def to_ref(east,north):
    """Convert a coordinate to a national grid reference."""

    # Work out the 100km and 10km squares...

    km10e = (east //100000)*100
    km10n = (north//100000)*100

    km100e = (km10e // 500) * 500
    km100n = (km10n // 500) * 500

    # Actually, the 10km square is relative to the base of the 100km square

    km10e  = km10e - km100e
    km10n  = km10n - km100n

    # Tuples for convenience

    km10  = (km10e,  km10n)
    km100 = (km100e, km100n)

    try:
        prefix = tup100[km100] + tup10[km10]
    except:
        print("Coordinate %d,%d does not make sense"%(east,north))
        print("It is not in the area supported by the National Grid")
        return

    east  = east  % 100000
    north = north % 100000

    print("Grid reference   (10m): %s %04d %04d"%(prefix,east//10,  north//10))
    print("Grid reference  (100m): %s  %03d  %03d"%(prefix,east//100, north//100))
    print("Grid reference (1000m): %s   %02d   %02d"%(prefix,east//1000,north//1000))


# ----------------------------------------------------------------------
def main():
    """Do it."""

    # Extract our arguments

    arg_list = sys.argv[1:]

    # What arguments do we have?

    arg_len = len(arg_list)

    if arg_len < 1 or arg_len > 3 or arg_list[0] == "-help":
        print(__doc__)
        return

    if arg_len == 2:
        try:
            east  = int(arg_list[0],10)
            north = int(arg_list[1],10)
        except:
            print(__doc__)
            return
        to_ref(east,north)
    else:
        from_ref(arg_list)


# If we're run from the shell, run ourselves

if __name__ == "__main__":
    main()
