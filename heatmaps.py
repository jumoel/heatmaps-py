#!/usr/bin/env python

import optparse
import os
         
def main():
  p = optparse.OptionParser()
  p.add_option('--background', '-b', help='Background image')
  p.add_option('--log', '-l', help='Log file')
  options, arguments = p.parse_args()

  if options.log is None or options.background is None:
    print "Both background and log are mandatory\n"
    p.print_help()
    exit(-1)

  if not os.path.exists(options.log):
    print "Log file \"" + options.log + "\" not found."
    exit(-1)

  if not os.path.exists(options.background):
    print "Background image \"" + options.log + "\" not found."
    exit(-1)

  parselog(options.log)

def parselog(logfile):
  print logfile


if __name__ == '__main__':
  main()
