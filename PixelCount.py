#!/usr/bin/env python

import sys
import os.path
from PIL import Image
import yaml
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from heapq import nlargest

with open("config.yaml") as f:
	config = yaml.load(f)

def readimage(filepath, colors):
	values = {}
	adjusted_values = {}
	source = Image.open(filepath)
	data = np.array(source)
	cval = (data[:,:,0].astype(np.uint32) << 16) | (data[:,:,1].astype(np.uint32) << 8) | data[:,:,2].astype(np.uint32)
	total = len(cval.flatten())
	print 'loaded {0} pixels'.format(total)
	uniques = np.unique(cval, return_counts = 1)
	print 'found {0} unique colors'.format(len(uniques[0]))
	values = dict(zip(uniques[0], uniques[1]))
	filtervalue = min(nlargest(colors + 1, values.values()))
	print 'filtering to {0} colors with minvalue {1}'.format(colors, filtervalue)
	for key in values.keys():
		if values[key] >= filtervalue:
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
	# Delete statistics for the background (white) area.
	del(adjusted_values[16777215])
	return adjusted_values, total

def pixel_counter(name):
	if name not in config:
		print 'Invalid name: "{0}".'.format(name)
		print 'Choose one of: {0}.'.format(config.keys())
		sys.exit(-1)
	map_config = config[name]

	filename = os.path.join('maps', name + '.png')
	colors = map_config['ncolors']
	# Calculate the linear scale in meters per pixel.
	linear_scale = float(map_config['scale_meters']) / map_config['scale_pixels']
	# Calculate the corresponding area scale in hectares per pixel.
	# 1 ha = (100 m)**2.
	area_scale = (linear_scale / 100) ** 2
	print 'Converting "{0}" with {1} colors and scale {2:.4g} ha / pix'.format(
		name, colors, area_scale)

	# Analyze the image pixel data.
	values, total = readimage(filename, colors)

	# Display a pie chart of results.
	sizes = []
	labels = []
	colors = []
	for element in values.keys():
		sizes.append((float(values[element])/total)*100)
		hectares = "{:.3f} ha".format(values[element] * area_scale)
		labels.append(hectares)
		colors.append("#"+str("%06x"%element))
	patches, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors,autopct="%1.1f%%",startangle=90)
	for text in texts:
		text.set_fontsize(9)
	for text in autotexts:
		text.set_fontsize(9)
	plt.axis("equal")
	plt.suptitle(name, fontsize='x-large')
	plt.savefig(os.path.join('charts', name + '.png'))
	if len(sys.argv) >= 3 and sys.argv[2] == "--display":
		plt.show()
	plt.clf()

if __name__ == "__main__":
	name = sys.argv[1]
	if name == "ALL":
		for mapfile in config.keys():
			pixel_counter(mapfile)
	else:
		pixel_counter(name)