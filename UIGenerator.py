# coding=utf-8
import json
import unicodedata


# Metodo que cria a árvore de diretórios no html recursivamente.
def generateFileTreePage(jsonFile):
	html = open('templates/mainPage.html','r').read()
	html += unicodedata.normalize('NFKD', generateFileTreeHTML(jsonFile,"")).encode('ascii','ignore')
	html += "</ul></body></html>"
	print html
	return html


def generateFileTreeHTML(jsonFile, currentParent):
	html = ""
	for jsonElement in jsonFile:
		if jsonElement["type"] == "dir":
			currentDir = jsonElement["name"] 
			html += "<li> <img src=\"/static/assets/dir.png\"> " + "<a href=\"/dirPage" + currentParent + "/" + currentDir + "\">" + currentDir + "</a>"
			html += "<ul>" + generateFileTreeHTML(jsonElement["list"], currentParent + "/" + currentDir) + "</ul>"
			html += "</li>"
		elif jsonElement["type"] == "file":
			file = jsonElement["name"]
			html += "<li><img src=\"/static/assets/file.png\"> " + "<a href=\"/filePage" + currentParent + "/" + file + "\">" + file + "</a></li>"
	return html

# Método que cria a tela de informações do server.
def generateSystemInfoHTML(systemCapacity,filesDistribution,numberOfFiles,activeNodes):
    html = open('templates/serverInfo.html', 'r').read()
    html = html.replace("#SYSTEM_CAPACITY#",str(systemCapacity))
    html = html.replace("#NUMBER_OF_FILES#", str(numberOfFiles))
    html += "<B>Active users:</B><br>"
    for node in activeNodes:
        html += str(node) + "<br>"
    html += "<B>File distribution:</B><br>"
    for element in filesDistribution:
        html += str(element['username']) + ": " + str(element['file']) + "<br>"
    html += "</body></html>"
    return html