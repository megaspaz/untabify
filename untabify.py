#!/usr/bin/env python
#
# Copyright (c) 2005, megaspaz
# All Rights Reserved.
#
# Script Name: untabify.py

"""This script will replace tabs with the specified number of spaces.

This script opens up a file, reads its output, and then replaces all tabs
with the specified number of spaces.

Usage: ./untabify [--help|-h] --file[-f]=<file> --space_count[-s]=<integer number>
  -f --file         The file to process. Required.
  -s --space_count  Replace tabs with this number of spaces. Default: 2 
                    Optional. 
  -h --help         Print this and exit.

"""

__author__ = "megaspaz <megaspaz2k7 <at> gmail.com>"

import fileinput
import getopt
import re
import sys

# Constants
_DEF_NUM = 2

def GetOptions():
  """This function gets the options from sys.arg

    This function will parse sys.arg to get the file to process as well as the
    number of spaces to replace tabs with.

    Args:
      None

    Returns:
      # The file to process as string.
      '/tmp/foo'
      # The number of spaces to replace '\t' with as integer.
      2

  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:hs:', 
      ['help', 'file=', 'space_count='])

    # Process the arguments.
    which_file = ''
    num = ''
    for option, value in opts:
      if option in ("-h", "--help"):
        return None, None, 0
      if option in ("-f", "--file"):
        which_file = value.strip()
      elif option in ("-s", "--space_count"):
        num = value.strip()
      else:
        raise KeyError('Bad arguments.')

    # Check to see if all required arguments were specified.
    if which_file == '':
      raise KeyError('Missing required argument.')

    if num == '':
      num = _DEF_NUM
    else:
      # Check to see that num is an integer.
      num_regex = re.compile('^\d+$')
      get_match = num_regex.match(num)
      if not get_match:
        sys.stderr.write('--space_count: Invalid value. '
          'Using default value of %s\n' % _DEF_NUM)
        num = _DEF_NUM
      else:
        # Check if num is greater than 0.
        if int(num) < 1:
          sys.stderr.write('--space_count: Invalid value. ' 
            'Using default value of %s\n' % _DEF_NUM)
          num = _DEF_NUM

    return which_file, int(num), 0

  except (getopt.GetoptError, KeyError), err:
    str_err = '%s\n\n%s' % (str(err), __doc__)
    sys.stderr.write(str_err)
    return None, None, -1

def Untabify(filename, spacecount):
  # Set up the space count to replace tabs with.
  str_space = ' ' * spacecount
  # Open the file and edit in place.
  fd = fileinput.FileInput(filename, 1)
  for line in fd:
    # use stdout since with fileinput uses it to edit file in place.
    sys.stdout.write(line.replace('\t', str_space))

  fd.close()

def main():
  try:
    # Get the options.
    which_file, num, ret_val = GetOptions()
    if ret_val:
      return ret_val
    else:
      if which_file is None:
        # -h/--help was specified.
        print '%s\n' % __doc__
        return ret_val

    # Process the file.
    Untabify(which_file, num)

    return 0

  except (IOError, OSError, MemoryError), err:
    sys.stderr.write('%s\n' % str(err))
    return 1 

if '__main__' == __name__:
  sys.exit(main())

