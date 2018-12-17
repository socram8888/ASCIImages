#!/usr/bin/env python3

import argparse
from PIL import Image

def rgbcompare(a, b):
	rd = a[0] - b[0]
	gd = a[1] - b[1]
	bd = a[2] - b[2]

	return 2 * rd * rd + 4 * gd * gd + 3 * bd * bd

def binarize(rgba, fore):
	if rgba[3] < 128:
		return False

	return 

def getbinary(img, x, y, factor, cutoff):
	solid = 0

	for rx in range(factor):
		for ry in range(factor):
			rgba = img.getpixel((x + rx, y + ry))
			if rgba[3] < 128:
				continue

			if rgbcompare(rgba, (255, 255, 255)) < rgbcompare(rgba, (0, 0, 0)):
				solid += 1

	return solid / (factor * factor) >= cutoff

parser = argparse.ArgumentParser(description='ASCII-fy image')
parser.add_argument('image', help='image')
parser.add_argument('--factor', help='scale factor', default=1, type=int)
parser.add_argument('--cutoff', help='color cutoff when scaling', default=0.5, type=float)
args = parser.parse_args()

img = Image.open(args.image)
img = img.convert('RGBA')

for y in range(0, img.height, 2 * args.factor):
	lastFore = None
	lastBack = None

	for x in range(0, img.width, args.factor):
		upper = getbinary(img, x, y, args.factor, args.cutoff)
		lower = getbinary(img, x, y + args.factor, args.factor, args.cutoff)

		if upper:
			if lower:
				print('█', end='')
			else:
				print('▀', end='')
		else:
			if lower:
				print('▄', end='')
			else:
				print(' ', end='')

	print()
