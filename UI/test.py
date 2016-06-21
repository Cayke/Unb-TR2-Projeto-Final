import json

with open('templates/test.json') as data_file: 
		jsonFile = json.load(data_file)

print jsonFile

for jsonPart in jsonFile:
	print jsonPart["list"]

