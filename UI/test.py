import json


with open('templates/test.json') as data_file: 
		jsonFile = json.load(data_file)

for element in jsonFile:

	print jsonFile[element]
	# if element["dir"] is not None:
	# 	print element["dir"]


