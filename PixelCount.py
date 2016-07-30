#!/usr/bin/env python

import sys
import os.path
from PIL import Image
import yaml
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from heapq import nlargest

def readimage(filepath, colors):
	values = {}
	adjusted_values = {}
	print 'loading'
	source = Image.open(filepath)
	data = np.array(source)
	cval = (data[:,:,0].astype(np.uint32) << 16) | (data[:,:,1].astype(np.uint32) << 8) | data[:,:,2].astype(np.uint32)
	print 'counting'
	uniques = np.unique(cval)
	values = {}
	for unique in uniques:
		occurences = np.count_nonzero(cval==unique)
		values[unique] = occurences
	total = float(len(cval.flatten()))
	filtervalue = min(nlargest(colors, values.values()))
	print 'adjusting'
	for key in values.keys():
		if values[key] > filtervalue:
			adjusted_values[key] = values[key]
	for key in values.keys(): #Filters each color into the major color that it is mathematically nearest to.
		if values[key] < filtervalue:
			min_distance = 442 #The smallest integer that is larger than the maximum distance between two colors.
			for primary in adjusted_values.keys():
				colorp = ((primary >> 16) & 255, (primary >> 8) & 255, (primary) & 255)
				colork = ((key >> 16) & 255, (key >> 8) & 255, (key) & 255)
				distance = sqrt(((colorp[0]-colork[0])**2)+((colorp[1]-colork[1])**2)+((colorp[2]-colork[2])**2))
				if distance < min_distance:
					min_distance = distance
					adjusted_color = primary
			adjusted_values[adjusted_color] += 1
	else:
		return values, total
	del(adjusted_values[16777215])
	return adjusted_values, total

if __name__ == "__main__":

	with open("config.yaml") as f:
		config = yaml.load(f)

	name = sys.argv[1]
	if name not in config:
		print 'Invalid name: "{0}".'.format(name)
		print 'Choose one of: {0}.'.format(config.keys())
		sys.exit(-1)
	config = config[name]

	filename = os.path.join('maps', name + '.png')
	colors = config['ncolors']
	# Calculate the linear scale in meters per pixel.
	linear_scale = float(config['scale_meters']) / config['scale_pixels']
	# Calculate the corresponding area scale in hectares per pixel.
	# 1 ha = (100 m)**2.
	area_scale = (linear_scale / 100) ** 2
	print 'Converting "{0}" with {1} colors and scale {2:.4g} ha / pix'.format(
		name, colors, area_scale)

	values, total = readimage(filename, colors)
	print len(values)
	sys.exit(0)
	sizes = []
	labels = []
	colors = []
	for element in values.keys():
		sizes.append((float(values[element])/total)*100)
		hectares = "{:.1f} ha".format(values[element] * area_scale)
		labels.append(hectares)
		colors.append("#"+str("%06x"%element))
	print colors
	print labels
	plt.pie(sizes, labels=labels, colors=colors,autopct="%1.1f%%",startangle=90)
	plt.axis("equal")
	plt.suptitle(os.path.splitext(filename)[0])
	plt.show()
