# 
# Creator: Grant McGovern
# Date: 06/19/2014
# 
# Purpose: Creates JSON Doc compatible with Brat NLP Visualizer json format. 

import sys 
import csv
import json
import time # Let's see how long the script takes to execute
from collections import OrderedDict # used for keeping preset JSON order 


def main():
	startime = time.time()
	createInitialJSONDoc()
	print "Completed in %s seconds." % (time.time() - startime)

def createInitialJSONDoc():

	# Lists
	type_ = []
	labels_ = []
	bgColor_ = []
	category_ = []
	borderColor_ = []

	# Process CSV. handle (") if we find any, MySQL returns Queuries with " or ' wrappers sometimes.

	with open("CategoryNames.csv", "r") as infile, open("newCategoryNames.csv", "wb") as outfile:
		CSVinput = csv.reader(infile, skipinitialspace=True, quotechar="'")
		CSVoutput = csv.writer(outfile)
		number_of_rows = 0
		for row in CSVinput:
			number_of_rows = number_of_rows + 1
			for column, col in enumerate(row):
				if col.strip() == "'":
					row[column] = ''
			CSVoutput.writerow(row)
	
	print "%s Rows Read. \n" % number_of_rows
	
	# Slice into tuples with Category name & Oc/Noc value:

	with open("newCategoryNames.csv", "r") as types_file:
		data = list(tuple(rec) for rec in csv.reader(types_file, delimiter=','))

	# Categories / Labels:

	itr = len(data) # Unconventional way of doing this w/ a while loop. No idea why a for-loop
					# didn't do the trick. Will look into that time permitting.
	
	while itr:
		itr = itr -1

		types = [rec[0] for rec in data][itr]
		type_.append(types)
		
		choppedLabel = [rec[0] for rec in data][itr][0:4] # Grabs the first 4 characters for label abbreviation
		labels_.append(choppedLabel)
		
		category = [rec[1] for rec in data][itr]
		category_.append(category)
		
		
	for (label, types) in zip(labels_, type_):
		newLabels = "%s, %s" % (types, label)

	# bgColors:

	for category in category_:
		if category == "NOC": 
			# Red 
			bgColorHexValue = "#ff7f8d"
			bgColor_.append(bgColorHexValue)
		elif category == "OC":
			# Yellow
			bgColorHexValue = "#f7de45"
			bgColor_.append(bgColorHexValue)
		elif category == "WHILE":
			# Light Yellow#F0E293
			bgColorHexValue = "F0E293"
			bgColor_.append(bgColorHexValue)
		elif category == "WHERE":
			# Light Red 
			bgColorHexValue = "#ffa5af"
			bgColor_.append(bgColorHexValue)
		elif category == "COMPARISON":
			# Brown
			bgColorHexValue = "#b29b59"
			bgColor_.append(bgColorHexValue)

	# borderColor

	for types in type_: # used again just to limit iterations 
		borderColor_.append("darken")

	# construct the doc

	desiredJson = OrderedDict([('type', ""), ('labels', '' ), ('bgColor', ''), ('borderColor', '')])

	with open("bratEntities.js", "wb") as JSONout:

		for (category_type, updatedLabels, bgColors, borderColors) in zip(type_, labels_, bgColor_, borderColor_):
			desiredJson["type"] = category_type
			desiredJson["labels"] = [category_type, (updatedLabels)]
			desiredJson["bgColor"] = bgColors
			desiredJson["borderColor"] = borderColors
			# TODO: Examine how to remove indented whitespace w/ JSON dump method and labels. This may screw up JSON interpreter, 
			# however, it should ignore unecessary whitespace. Anyhow, I would like to get rid of this. 
			JSONout.write(json.dumps(desiredJson, sort_keys = False, indent = 4, separators=(',', ': ')) + ',\n')

if __name__ == "__main__":
	main()


