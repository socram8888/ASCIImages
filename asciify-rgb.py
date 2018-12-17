#!/usr/bin/env python3

import argparse
from math import *
from PIL import Image

COLORS = {
	0x30: (  0,   0,   0),
	0x31: (128,   0,   0),
	0x32: (  0, 128,   0),
	0x33: (128, 128,   0),
	0x34: (  0,   0, 128),
	0x35: (128,   0, 128),
	0x36: (  0, 128, 128),
	0x37: (192, 192, 192),
	0x90: (128, 128, 128),
	0x91: (255,   0,   0),
	0x92: (  0, 255,   0),
	0x93: (255, 255,   0),
	0x94: (  0,   0, 255),
	0x95: (255,   0, 255),
	0x96: (  0, 255, 255),
	0x97: (255, 255, 255)
}

def rgbcompare(a, b):
	rd = a[0] - b[0]
	gd = a[1] - b[1]
	bd = a[2] - b[2]

	return 2 * rd * rd + 4 * gd * gd + 3 * bd * bd

def getBestMatch(targetColor):
	bestCode = None
	bestDiff = inf

	for ttyCode, ttyColor in COLORS.items():
		curDiff = rgbcompare(targetColor, ttyColor)
		if curDiff < bestDiff:
			bestCode = ttyCode
			bestDiff = curDiff

	return bestCode

def setFore(color):
	print('\x1B[%02xm' % color, end='')

def setBack(color):
	if lower > 0x40:
		print('\x1B[10%xm' % (lower % 16), end='')
	else:
		print('\x1B[4%xm' % (lower % 16), end='')
	
parser = argparse.ArgumentParser(description='ASCII-fy image')
parser.add_argument('image', help='image')
args = parser.parse_args()

img = Image.open(args.image)
img = img.convert('RGB')

print('\x1B[0m', end='')

for y in range(0, img.height, 2):
	lastFore = None
	lastBack = None

	for x in range(0, img.width):
		upper = getBestMatch(img.getpixel((x, y + 0)))
		lower = getBestMatch(img.getpixel((x, y + 1)))

		if upper == lower:
			if upper == lastBack:
				print(' ', end='')
			else:
				if upper != lastFore:
					setFore(upper)
					lastFore = upper
				print('█', end='')
		else:
			if upper == lastBack:
				if lower != lastFore:
					setFore(lower)
					lastFore = lower
				print('▄', end='')

			else:
				if upper != lastFore:
					setFore(upper)
					lastFore = upper
				if lower != lastBack:
					setBack(lower)
					lastBack = lower
				
				print('▀', end='')

	print('\x1B[0m')
