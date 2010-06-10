#!/usr/bin/env python

import optparse
import os
import Image # http://www.pythonware.com/products/pil/
from numpy import zeros # http://numpy.scipy.org/
         
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

  heatmap(options.log, options.background)

def lerp(a, b, t):
  return a + (b - a) * t

def parselog(logfile):
  f = open(logfile)

  xmin = float(f.readline().split(":")[1])
  ymin = float(f.readline().split(":")[1])
  zmin = float(f.readline().split(":")[1])
  xmax = float(f.readline().split(":")[1])
  ymax = float(f.readline().split(":")[1])
  zmax = float(f.readline().split(":")[1])

  f.readline() # Not used except by puny humans

  coords = []
  for line in f:
    splits = line.split(" , ")
    coords.append(tuple(map(float, splits)))

  parsed = { "xmin": xmin,
             "xmax": xmax,
             "ymin": ymin,
             "ymax": ymax,
             "zmin": zmin,
             "zmax": zmax,
             "coords": coords }

  return parsed

def heatmap(logfile, background):
  parsed = parselog(logfile)

  image = Image.open(background)

  width, height = image.size

  hmap = zeros((width, height))

  for t in parsed["coords"]:
    # do stuff
    
if __name__ == '__main__':
  main()
