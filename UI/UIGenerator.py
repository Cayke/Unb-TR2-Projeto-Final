import json
import unicodedata

def generateFileTreePage(jsonFile):
	html = "<html>"
	html += "<body>"
	html += "<title>Files</title>"
	html += "<ul>"
	html += generateFileTreeHTML(jsonFile,"")
	html += "</ul></body></html>"
	return unicodedata.normalize('NFKD', html).encode('ascii','ignore')


def generateFileTreeHTML(jsonFile, currentParent):
	html = ""
	for jsonElement in jsonFile:
		if jsonElement["type"] == "dir":
			currentDir = jsonElement["name"] 
			html += "<li> <img src=\"static/assets/dir.png\"> " + "<a href=\"dirPage" + currentParent + "/" + currentDir + "\">" + currentDir + "</a>"
			html += "<ul>" + generateFileTreeHTML(jsonElement["list"], currentParent + "/" + currentDir) + "</ul>"
			html += "</li>"
		elif jsonElement["type"] == "file":
			file = jsonElement["name"]
			html += "<li><img src=\"static/assets/file.png\"> " + "<a href=\"filePage" + currentParent + "/" + file + "\">" + file + "</a></li>"
	return html

with open('templates/test.json') as data_file: 
		jsonFile = json.load(data_file)

finalHTML = generateFileTreePage(jsonFile)

print type(finalHTML)
print(finalHTML)