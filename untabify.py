#!/usr/bin/env python3
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
  -s --space_count  Replace tabs with this number of spaces. Must be at least 1. Default: 2
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

def get_options():
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
    # pylint: disable=unused-variable
    opts, args = getopt.getopt(sys.argv[1:], 'f:hs:', ['help', 'file=', 'space_count='])

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
      raise ValueError('Missing required argument.')

    if num == '':
      num = _DEF_NUM
    else:
      # Check to see that num is an integer.
      if not re.compile(r'^\d+$').match(num) or int(num) < 1:
        raise ValueError('--space_count: Invalid value: %s' % num)

    return which_file, int(num), 0

  except (getopt.GetoptError, KeyError, ValueError) as err:
    str_err = '%s\n\n%s' % (str(err), __doc__)
    sys.stderr.write(str_err)
    return None, None, -1


def untabify(filename, spacecount):
  """Replace tab chars with number of spaces per tab."""

  # Open the file and edit in place.
  file_desc = fileinput.FileInput(filename, 1)
  for line in file_desc:
    # use stdout since with fileinput uses it to edit file in place.
    sys.stdout.write(line.replace('\t', ' ' * spacecount))

  file_desc.close()


def main():
  """Main method."""

  try:
    # Get the options.
    which_file, num, ret_val = get_options()
    if ret_val:
      return ret_val

    if which_file is None:
      # -h/--help was specified.
      sys.stdout.write('%s\n' % __doc__)
      return ret_val

    # Process the file.
    untabify(which_file, num)

    return 0

  except (IOError, OSError, MemoryError) as err:
    sys.stderr.write('%s\n' % str(err))
    return 1


if __name__ == '__main__':
  sys.exit(main())
