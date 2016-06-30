# coding=utf-8
import socket
import json
import base64
#import sys
#sys.path.insert(0, '/home/igor/Projetos/tr2-trabalhofinal')
import Define

class StubServer:

    __IP = '127.0.0.1'  # Server IP
    __PORTSERVER = 3301  # Server PORT
    __PORTCLIENT = 4578  # Client PORT to recive DHT files
    __ID = -1  # ID do usuário

    def __init__(self):
        self.server()

    def server(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.__IP, self.__PORTSERVER)
        tcp.bind(orig)
        tcp.listen(1)
        while True:
            con, cliente = tcp.accept()
            print ('Concetado por ', cliente)
            request = con.recv(2048)
            jsonrequest = json.loads(request)
            if int(jsonrequest["type"]) == Define.LOGIN:
                #success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                register = '{"responseStatus" : ' + str(Define.USERNOTREGISTER) + '}'
                con.send(register)
                con.close()
            elif int(jsonrequest["type"]) == Define.REGISTER:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                con.send(success)
                con.close()
            elif int(jsonrequest["type"]) == Define.UPLOAD:
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "id": 0}'
                con.send(success)
                con.close()
            elif int(jsonrequest["type"]) == Define.DOWNLOAD:
                datab64 = base64.b64encode('abcdefghijklmnopqrstuwxyz')
                success = '{"responseStatus" : ' + str(Define.SUCCESS) + ', "type" : "file", "data" : "' + datab64 +'"}'
                con.send(success)
                con.close()
            elif int(jsonrequest["type"]) == Define.DIRINFO:
                success = dict(responseStatus = Define.SUCCESS)
                con.send(json.dumps(success))
                con.close()


server = StubServer()
