from PIL import Image
from PIL import ImageColor
import sys

with open("colornames.tsv","r") as colorlist:
	colornames = dict()
	colorcodes = dict()
	lines = colorlist.readlines()
	for code,line in enumerate(lines):
		hexcode,colorname,light,hue = line.strip().split("\t")
		colornames[ImageColor.getrgb(hexcode)] = colorname
		colorcodes[colorname] = (chr(code + ord('A')), light, hue)

imagepath = sys.argv[1];
im = Image.open(imagepath)
im_rgb = im.convert("RGB")
im_names = list(map(colornames.get,list(im_rgb.getdata())))
im_codes = list(map(colorcodes.get,im_names))
width,height = im.size
codegrid = [[im_codes[x+width*y][0] for x in range(width)] for y in range(height)]
for line in codegrid:
	print("".join(line))
