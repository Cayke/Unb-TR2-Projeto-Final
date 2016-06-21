import json

def fileDistribution(json):
	html = generatePathTreeHTML(json)


def generatePathTreeHTML(json):
	for currentDir = json["dir"]:
		