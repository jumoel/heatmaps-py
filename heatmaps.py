#!/usr/bin/env python

import optparse
import os
import Image # http://www.pythonware.com/products/pil/
import ImageChops
import math
from numpy import *
import locale

import cProfile

dir = os.path.dirname(os.path.abspath(__file__))

def main():
  p = optparse.OptionParser()
  p.add_option('--background', '-b', help='Background image', default = dir + "\\whitedemo.png")
  p.add_option('--log', '-l', help='Log file')
  p.add_option('--dotsize', '-d', help="Size of the dots to place on the heatmap", default=15)
  p.add_option('--every', '-e', help="Parse every X log entries", default = 1)
  p.add_option('--dotmin', '-n', help="The minimum value for the dot color", default = 0)
  p.add_option('--death', '-q', action="store_true", dest="death", default = False)
  options, arguments = p.parse_args()

  if options.log is None:
    print "Log is mandatory\n"
    p.print_help()
    exit(-1)

  if not os.path.exists(options.log):
    print "Log file \"" + options.log + "\" not found."
    exit(-1)
    
  if not os.path.exists(options.background):
    print "Background image \"" + options.background + "\" not found."
    exit(-1)

  locale.setlocale(locale.LC_ALL, '')

  if not options.death:
    heatmap(options.log, options.background, int(options.dotsize), int(options.every), int(options.dotmin))
  else:
    deathmap(options.log, options.background, int(options.dotsize))

def lerp(t, a, b):
  return a + (b - a) * t

def clamp(x, xmin, xmax):
  if x < xmin:
    return xmin
  elif x > xmax:
    return xmax
  else:
    return x

def parselog(logfile):
  f = open(logfile)

  xmin = locale.atof(f.readline().split(":")[1])
  ymin = locale.atof(f.readline().split(":")[1])
  zmin = locale.atof(f.readline().split(":")[1])
  xmax = locale.atof(f.readline().split(":")[1])
  ymax = locale.atof(f.readline().split(":")[1])
  zmax = locale.atof(f.readline().split(":")[1])

  f.readline() # Not used except by puny humans

  coords = []
  for line in f:
    splits = line.split(" , ")
    coords.append(tuple(map(locale.atof, splits)))

  parsed = { "xmin": xmin,
             "xmax": xmax,
             "ymin": ymin,
             "ymax": ymax,
             "zmin": zmin,
             "zmax": zmax,
             "coords": coords }

  return parsed

# http://sol.gfxile.net/interpolation/
def smoothstep(x):
  return (x) * (x) * (3 - 2 * (x))

def smooth(x):
  return x #smoothstep(x)

# Generate a dot for a point in the heatmap
def gendot(size, minvalue):
  img = Image.new("RGB", (size, size), "white")
  
  middle = size / 2
  maxdist = size / 2

  for x in range(size):
    for y in range(size):
      xx = x - middle
      yy = y - middle

      dist = clamp(math.sqrt(xx**2 + yy**2), 0, maxdist)
      
      rgb = int(lerp(smooth(dist/(size/2)), minvalue, 255))

      img.putpixel((x, y), (rgb, rgb, rgb))

  img.save("dot.png")

  return img

def gendeathdot(dotsize):
  img = Image.open(dir + "\\skull.png")

  return img.resize((dotsize, dotsize))

def deathmap(logfile, background, dotsize):
  parsed = parselog(logfile)

  image = Image.open(background)

  width, height = image.size

  xmin = parsed["xmin"]
  zmin = parsed["zmin"]
  xgrid = (parsed["xmax"] - xmin) / width
  zgrid = (parsed["zmax"] - zmin) / height

  heatimage = Image.new("RGBA", image.size, (255, 255, 255, 0))
  dot = gendeathdot(dotsize)

  for t in parsed["coords"]:
    x = int(round((t[0] - xmin) / xgrid))
    z = int(round((t[2] - zmin) / zgrid))
    x = int(round(x - dotsize / 2))
    z = int(round(z - dotsize / 2))

    heatimage.paste(dot, (x, z))

  heatimage.save(logfile + ".png")

def heatmap(logfile, background, dotsize, every, minvalue):
  parsed = parselog(logfile)

  image = Image.open(background)

  width, height = image.size

  xmin = parsed["xmin"]
  zmin = parsed["zmin"]
  xgrid = (parsed["xmax"] - xmin) / width
  zgrid = (parsed["zmax"] - zmin) / height

  heatimage = Image.new("RGBA", image.size, "white")
  dot = gendot(dotsize, minvalue)
  tmptmp = Image.new("RGBA", image.size, "white")
  #heatarr = asarray(heatimage).astype("locale.atof")

  i = 1

  # Parse the log and set heatmap
  for t in parsed["coords"]:
    if i % every == 0:
      x = int(round((t[0] - xmin) / xgrid))
      z = int(round((t[2] - zmin) / zgrid))
      x = int(round(x - dotsize / 2))
      z = int(round(z - dotsize / 2))
    
      tempimg = Image.new("RGBA", image.size, "white")
      tempimg.paste(dot, (x, z))
    
      tmptmp = ImageChops.multiply(tmptmp, tempimg)

    i = (i + 1) % every

    #temparr = asarray(tempimg).astype("locale.atof")
    
    #heatimage = ImageChops.multiply(heatimage, tempimg)
    #heatarr = heatarr + temparr;
    
 # heatimage = Image.fromarray(heatarr)
  heatimage = ImageChops.multiply(heatimage, tmptmp)
  heatimage.save(logfile + ".png")

if __name__ == '__main__':
  #psyco.full()
  #cProfile.run("main()", "benchmark.txt")
  main()
