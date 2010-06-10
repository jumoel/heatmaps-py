#!/usr/bin/env python

import optparse
         
def main():
  p = optparse.OptionParser()
  p.add_option('--background', '-b', help='Background image')
  p.add_option('--log', '-l', help='Log file')
  options, arguments = p.parse_args()

  if options.log is None or options.background is None:
    print "Both background and log are mandatory\n"
    p.print_help()
    exit(-1)
             
if __name__ == '__main__':
  main()
