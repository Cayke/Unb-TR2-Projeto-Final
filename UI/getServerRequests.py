# -*- coding: utf-8 -*-
import json

# Envio de mensagens ao servidor
def countFiles():
	print "Descobrir número de arquivos"

def totalUsedSize():
	print "Quantidade de dados utilziada"

def fileDistribution():
	print "File distribution"
	with open('templates/test.json') as data_file: 
			jsonFile = json.load(data_file)
	return jsonFile
	
def countNodes():
	print "Nós ativos"

def newDir(name, path):
	print "Novo diretório"

def sendFile(path, file):
	print "Enviar arquivo"

def renameDir(newName, path):
	print "Novo nome: "+ newName

def renameFile(newName, path):
	print "Novo nome: "+ newName	

def removeDir(path):
	print "Diretório removido: " + path

def removeFile(name, path):
	print "Arquivo removido: " + name

def downloadFile(path):
	print path