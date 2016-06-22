# -*- coding: utf-8 -*-
import json

# Envio de mensagens ao servidor

def login(userName):
	print userName

def logout(userName):
	print logout

def getServerInfo():
	return "Descobrir número de arquivos, quantidade de dados e número de users conectados"

def fileDistribution():
	print "File distribution"
	with open('templates/test.json') as data_file: 
			jsonFile = json.load(data_file)
	return jsonFile

def newDir(name, path):
	print "Novo diretório"

def renameDir(newName, path):
	print "Novo nome: "+ newName

def renameFile(newName, path):
	print "Novo nome: "+ newName	

def removeDir(path):
	print "Diretório removido: " + path

def removeFile(name, path):
	print "Arquivo removido: " + name

def downloadFile(path):
	file = open('templates/teste.txt','r').read()
	print path
	return file

def uploadFile(type,name,data):
	print name
