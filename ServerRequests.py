# -*- coding: utf-8 -*-
import json
from ClientInterface import *
import Define

# Envio de mensagens ao servidor
class ServerRequests:
	"""docstring for ClassName"""
	clientInterface = None

	def __init__(self):
		self.clientInterface = ClientInterface()
		print "Teste"

	def login(self,userName):
		response = self.clientInterface.login(userName)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def logout(self,userName):
		self.clientInterface.logout()
		return True

	def getServerInfo(self):
		return "Descobrir número de arquivos, quantidade de dados e número de users conectados"

	def fileDistribution(self):
		response = self.clientInterface.dirinfo()
		if self.__errorVerification(response):
			print "Message"
			print response['msg']
			return response['msg']
		else:
			return None
		
	def newDir(self,name, path):
		print "Novo diretório"
		response = self.clientInterface.newDir(path,name)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def renameDir(self,newName, path):
		print "Novo nome: "+ newName
		response = self.clientInterface.renamedir(path,newName)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def renameFile(self,newName, path):
		print "Novo nome: "+ newName	
		response = self.clientInterface.renamefile(path,newName)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def removeDir(self,path):
		print "Diretório removido: " + path
		response = self.clientInterface.removedir(path)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def removeFile(self,name, path):
		print "Arquivo removido: " + name
		response = self.clientInterface.removefile(path)
		if self.__errorVerification(response):
			return True
		else:
			return False		

	def downloadFile(self,path):
		response = self.clientInterface.download(path)
		if self.__errorVerification(response):
			return response['msg']
		else:
			return None

	def uploadFile(self,data,path):
		response = self.clientInterface.upload(data,path)
		if self.__errorVerification(response):
			return True
		else:
			return False

	def __errorVerification(self,response):
		print response['code']
		if Define.SUCCESS == response['code']:
			return True
		else:
			return False

