#!/usr/bin/env python3

import sys
from itertools import *

TO_BITS = {
	' ': 0,
	'▀': 1,
	'▄': 2,
	'█': 3
}

FROM_BITS = {v: k for k, v in TO_BITS.items()}

files = [open(x) for x in sys.argv[1:]]

while len(files) > 0:
	result = bytearray()
	filteredFiles = list()

	for file in files:
		line = file.readline()
		if line != '':
			filteredFiles.append(file)
			line = line.rstrip('\r\n')

			missing = len(line) - len(result)
			if missing > 0:
				result.extend(bytearray(missing))

			for pos in range(len(line)):
				result[pos] |= TO_BITS[line[pos]]
		else:
			file.close()

	if len(filteredFiles) > 0:
		for c in result:
			print(FROM_BITS[c], end='')
		print()

	files = filteredFiles
