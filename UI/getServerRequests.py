# -*- coding: utf-8 -*-

import callbacksServerRequest as CK

# Envio de mensagens ao servidor
def countFiles():
	print "Descobrir número de arquivos"

def totalUsedSize():
	print "Quantidade de dados utilziada"

def fileDistribution():
	print "File distribution"

def countNodes():
	print "Nós ativos"

def newDir(name, path):
	print "Novo diretório"

def sendFile(file):
	print "Enviar arquivo"

def renameDir(newName, path):
	print "Novo nome: "+ newName

def renameFile(newName, path):
	print "Novo nome: "+ newName	

def removeDir(path):
	print "Diretório removido: " + path

def removeFile(name, path):
	print "Arquivo removido: " + name