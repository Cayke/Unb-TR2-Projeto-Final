# -*- coding: utf-8 -*-
import json
from ClientInterface import *
import Define

# Classe responsável por realizar requisições com o server do cliente. Utilizado pelo gerenciador do HTML.
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
		response = self.clientInterface.infofiles()
		if self.__errorVerification(response):
			return response
		else:
			return None

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
		response = self.clientInterface.createdir(path,name)
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

	def removeFile(self, path):
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

