# coding=utf-8
import socket
import json
import base64
#import sys
#sys.path.insert(0, '/home/igor/Projetos/tr2-trabalhofinal')
import Define

class StubServer:

    __IP = '127.0.0.1'  # Server IP
    __PORTSERVER = 5000  # Server PORT
    __PORTCLIENT = 4578  # Client PORT to recive DHT files
    __ID = -1  # ID do usuário

    def __init__(self):
        self.server()

    def server(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.__IP, self.__PORTSERVER)
        tcp.bind(orig)
        tcp.listen(1)
        con, cliente = tcp.accept()
        while True:

            print ('Concetado por ', cliente)
            request = con.recv(2048)
            jsonrequest = json.loads(request)

            if int(jsonrequest["type"]) == Define.LOGIN:
                #success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                register = '{"responseStatus" : ' + str(Define.USERNOTREGISTER) + '}'
                con.send(register)
            elif int(jsonrequest["type"]) == Define.REGISTER:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.UPLOAD:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.DOWNLOAD:
                tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                orig = ('127.0.0.1', 3301)
                tcp2.bind(orig)
                tcp2.listen(1)
                datab64 = base64.b64encode('abcdefghijklmnopqrstuwxyz')
                #success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "type" : "file", "data" : "' + datab64 +'"}'
                success = dict(responseStatus=str(Define.SUCCESS), type="hash", hashName='dsafasdf', node='127.0.0.1:3301')
                con.send(json.dumps(success))
                con2, cliente = tcp2.accept()
                request = con2.recv(2048)
                success = dict(responseStatus=Define.SUCCESS, type='file', data=datab64)
                con2.send(json.dumps(success))
                con2.close()
                tcp2.close()
            elif int(jsonrequest["type"]) == Define.DIRINFO:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "dir" : "/"}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.CREATEDIR:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + '}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.RENAMEDIR:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + '}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.REMOVEDIR:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + '}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.RENAMEFILE:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + '}'
                con.send(success)
            elif int(jsonrequest["type"]) == Define.REMOVEFILE:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + '}'
                con.send(success)


server = StubServer()
