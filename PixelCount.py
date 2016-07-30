import Image
import yaml
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from os import path

with open("config.yaml") as f:
	config = yaml.load(f)

def readimage(filepath, filterpercent = 0.2):
	values = {}
	adjusted_values = {}
	source = Image.open(filepath)
	data = np.array(source)
	cval = (data[:,:,0].astype(np.uint32) << 16) | (data[:,:,1].astype(np.uint32) << 8) | data[:,:,2].astype(np.uint32)
	uniques = np.unique(cval)
	values = {}
	for unique in uniques:
		occurences = np.count_nonzero(cval==unique)
		values[unique] = occurences
	total = float(len(cval.flatten()))
	filtervalue = total/(100/filterpercent)
	if filtervalue > 0:
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
	filename = raw_input("Enter the file path to count pixels for: ")
	values, total = readimage(filename)
	sizes = []
	labels = []
	colors = []
	for element in values.keys():
		sizes.append((float(values[element])/total)*100)
		hectares = "{:.1f} ha".format(values[element]*config["scale"])
		'''
		if element in config["legend"].keys():
			labels.append((str(config["legend"][element])+" : "+hectares))
		else:
			labels.append(("#"+str("%06x"%element)+" : "+hectares))
		'''
		labels.append(hectares)
		colors.append("#"+str("%06x"%element))
	print colors
	print labels
	plt.pie(sizes, labels=labels, colors=colors,autopct="%1.1f%%",startangle=90)
	plt.axis("equal")
	plt.suptitle(path.splitext(filename)[0])
	plt.show()