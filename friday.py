#!/usr/bin/env python3

"""friday -- give the date of a week's Friday

Usage: friday [<when>]

Arguments may also be:

<when> may be:

    last                last week
    next                next week
    this                this week (same as not giving <when>)
    yyyy/mm/dd          the Friday for that week
    yyyy/mm/dd          ditto
    dd-mm-yyyy          ditto
    dd-mm-yyyy          ditto
    -help               print out this information and exit

Otherwise, the currrent week's Friday will be calculated and reported.

Following the conventions I needed when this was written, Saturday and
Sunday are taken to belong to the week of the following Friday.
"""

import sys
import datetime
import re

ddmmyyyy1_re = re.compile("\d\d/\d\d/\d\d\d\d")
yyyymmdd1_re = re.compile("\d\d\d\d/\d\d/\d\d")
ddmmyyyy2_re = re.compile("\d\d-\d\d-\d\d\d\d")
yyyymmdd2_re = re.compile("\d\d\d\d-\d\d-\d\d")

seven_days = datetime.timedelta(7)

def calc_friday(today=None):
  """Given a datetime ``date``, calculate Friday's ``date``
  """
  if today is None:
    today = datetime.date.today()
  weekday = today.weekday()       # 0 = Monday
  if weekday == 4:
    friday = today
  elif weekday < 4:
    friday = today + datetime.timedelta(4 - weekday)
  elif weekday == 5:              # Saturday
    friday = today + datetime.timedelta(6)
  elif weekday == 6:              # Sunday
    friday = today + datetime.timedelta(5)
  else:
    raise ValueError("Unexpected weekday number %d for date %s"%(weekday,today))
  return friday

def calc_friday_from_parts(dd,mm,yyyy):
    yyyy = int(yyyy)
    month = int(mm)
    day = int(dd)
    return calc_friday(datetime.date(yyyy,month,day))


def main():
  args = sys.argv[1:]

  if len(args) == 0:
    friday = calc_friday()
  elif len(args) == 1:
    when = args[0]
    if when == "last":
      friday = calc_friday() - seven_days
    elif when == "next":
      friday = calc_friday() + seven_days
    elif when == "this":
      friday = calc_friday()
    elif ddmmyyyy1_re.match(when):
      dd,mm,yyyy = when.split("/")
      friday = calc_friday_from_parts(dd,mm,yyyy)
    elif yyyymmdd1_re.match(when):
      year,mm,dd = when.split("/")
      friday = calc_friday_from_parts(dd,mm,year)
    elif ddmmyyyy2_re.match(when):
      dd,mm,yyyy = when.split("/")
      friday = calc_friday_from_parts(dd,mm,yyyy)
    elif yyyymmdd2_re.match(when):
      year,mm,dd = when.split("/")
      friday = calc_friday_from_parts(dd,mm,year)
    elif when in ("-h", "-help", "--help"):
      print(__doc__)
      return
    else:
      print("Unrecognised argument '%s'"%when)
      print(__doc__)
      return
  else:
    print(__doc__)
    return

  print(friday)

if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# vim: set filetype=python expandtab tabstop=4 shiftwidth=4:
# [X]Emacs local variables declaration - place us into python mode
# Local Variables:
# mode:python
# py-indent-offset:4
# End:
