# coding=utf-8
import socket
import json
import base64
import Define
import os
import signal
import time
import threading
import netifaces as ni


class ClientInterface:

    __IP = '127.0.0.1'   # Server IP
    __PORTSERVER = 5000  # Server PORT
    __PORTCLIENT = 4578  # Client PORT to recive DHT files
    __ID = -1            # ID do usuário
    __tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __username = ''
    __serverdown = False
    __keepalivetime = 30

    def __init__(self):
        self.__th = threading.Thread(target=self.dht, args=())

    # Register a user
    # param: username - The username to register in database
    # return: json {code,msg}
    def __register(self, username):

        jsonmsg = dict(username=username, type=Define.REGISTER)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = jsonresponse["id"]
            self.__username = username
            #if not self.__th.isAlive():
                #self.__th.start()
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg="Register Error")


    # Login a user
    # param: username - The username to login
    # return: json {code,msg}
    def login(self, username):

        try:
            self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dest = (self.__IP, self.__PORTSERVER)
            # self.tcp.bind(('', self.__PORTCLIENT))
            self.__tcp.connect(dest)
        except socket.error as msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + str(msg[1])
            error = '{"code" : "' + str(Define.FAILEDCREATESOCK) + '", "msg" :  "Failed to create socket"}'
            jsonerror = json.loads(error)
            return jsonerror

        # Call keepalive in 30 seconds
        #signal.signal(signal.SIGALRM, self.__keepalive)
        #signal.alarm(self.__keepalivetime)

        jsonmsg = dict(username=username, type=Define.LOGIN)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = int(jsonresponse["id"])
            self.__username = username
            #if not self.__th.isAlive():
                #self.__th.start()
            return dict(code=Define.SUCCESS, msg='Success')
        elif int(jsonresponse["responseStatus"]) == Define.USERNOTREGISTER:
            return self.__register(username)
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])



    # Upload file to server
    # param: data - Tho content of the file
    # param: path - The path of the file
    # return: json {code,msg}
    def upload(self, data, path):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        datab64 = base64.b64encode(data)
        jsonmsg = dict(path=path, data=datab64, type=Define.UPLOAD)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])

    # Download file from server
    # param: path - The path of the file including file name
    # return: SUCCESS/ERROR CODE (if success file will be writen in a folder)
    def download(self, path):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(method='path', path=path, type=Define.DOWNLOAD)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            if jsonresponse["type"] == 'file':
                return dict(code=Define.SUCCESS, msg=base64.b64decode(jsonresponse["data"]))
            elif jsonresponse["type"] == 'hash':
                jsonmsg = dict(method='hash', hash=str(jsonresponse["hashName"]), type=Define.DOWNLOAD)
                msg = json.dumps(jsonmsg)
                ip, port = jsonresponse["node"].split(':')
                response = self.__sendMSG(msg, ip, int(port))
                try:
                    jsonresponse = json.loads(response)
                except:
                    return dict(code=Define.ERROTCP, msg='Download failed')

                if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
                    return dict(code=Define.SUCCESS, msg=base64.b64decode(jsonresponse["data"]))
                else:
                    return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            else:
                return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])

        else:
            return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])

    def dirinfo(self):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(type=Define.DIRINFO)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg=jsonresponse["tree"])
        else:
            return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])

    # Create directory
    # param: path - The path of the new directory without the new directory
    # param: namedir - The name of the new directory
    # return: SUCCESS/ERROR CODE
    def createdir(self, path, namedir):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        if path[-1:] == '/':
            path = path[:-1]

        path = os.path.join(path, namedir)
        jsonmsg = dict(path=path, type=Define.CREATEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    # Rename directory
    # param: path - The path of the new directory included the directory to rename
    # param: namedir - The  new name of the directory
    # return: SUCCESS/ERROR CODE
    def renamedir(self, path, newnamedir):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        if path[-1:] == '/':
            path = path[:-1]

        jsonmsg = dict(path=path, newname=newnamedir, type=Define.RENAMEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    # Remove directory
    # param: path - The path of the new directory included the directory to remove
    # return: SUCCESS/ERROR CODE
    def removedir(self, path):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(path=path, type=Define.REMOVEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    # Rename file
    # param: path - The path of the old file included the file to rename
    # param: namedir - The  new name of the file
    # return: SUCCESS/ERROR CODE
    def renamefile(self, path, newname):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(path=path, newname=newname, type=Define.RENAMEFILE)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    # Remove file
    # param: path - The path of the file included the file to remove
    # return: SUCCESS/ERROR CODE
    def removefile(self, path):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(path=path, type=Define.REMOVEFILE)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg='Success')
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    def infofiles(self):
        if self.__ID == -1:
            return dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")

        jsonmsg = dict(type=Define.INFOFILES)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        try:
            jsonresponse = json.loads(response)
        except:
            self.__ID = -1
            return dict(code=Define.ERROJSON, msg="Decoding JSON has failed. Connection down")

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            return dict(code=Define.SUCCESS, numberOfFiles=jsonresponse['numberOfFiles'], capacityOfSystem=jsonresponse['capacityOfSystem'], filesDistribution=jsonresponse['filesDistribution'],  activeNodes=jsonresponse['activeNodes'])
        else:
            return dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])

    def logout(self):
        self.__tcp.close()

    def __sendMSG(self, msg, ip, port):
        try:
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + str(msg[1])
            error = '{"code" : "' + str(Define.FAILEDCREATESOCK) + '", "msg" :  "Failed to create socket"}'
            jsonerror = json.loads(error)
            return jsonerror

        dest = (ip, port)

        try:
            con.connect(dest)
            con.send(msg)
        except socket.error:
            # Send failed
            print 'Send failed'
            error = '{"responseStatus" : "' + str(Define.SENDFAILED) + '", "msg" :  "Send Failed"}'
            return error

        rtn = con.recv(2048)
        con.close()

        return rtn

    def __sendMSGtoserver(self, msg):
        try:
            self.__tcp.send(msg)
        except socket.error:
            # Send failed
            print 'Send failed'
            error = '{"responseStatus" : "' + str(Define.SENDFAILED) + '", "msg" :  "Send Failed"}'
            return error

        try:
            rtn = self.__tcp.recv(2048)
        except:
            return '{"responseStatus" : "' + str(Define.ERROTCP) + '", "msg" :  "Server didnt responde"}'

        return rtn

    def __downloadserverhash(self, hash):
        jsonmsg = dict(method='hash', hash=hash, type=Define.DOWNLOAD)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)
        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            return dict(code=Define.SUCCESS, msg=base64.b64decode(jsonresponse["data"]))
        else:
            return dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])

    def __reconnect(self):
        rtn = self.login(self.__username)
        try:
            jsonrtn = json.loads(rtn)
        except:
            self.__ID = -1
            return dict(code=jsonrtn["responseStatus"], msg="Decoding JSON has failed. Connection down")

        if int(jsonrtn['responseStatus']) == Define.SUCCESS:
            return dict(responseStatus=Define.SUCCESS, msg="Reconnected")
        else:
            return dict(responseStatus=Define.SERVERDOWN, msg="Server down")

    def __keepalive(self, signum, stack):

        # Call keepalive in 30 seconds
        #signal.signal(signal.SIGALRM, self.__keepalive)
        #signal.alarm(self.__keepalivetime)

        msg = dict(type=Define.KEEPALIVE)
        print 'keepalive: ' + time.ctime()
        try:
            self.__tcp.send(json.dumps(msg))
        except socket.error:
            # Send failed
            print 'Send failed Keep alive: Connection closed'
            '''print 'Trying to reconnect'
            rtn = self.reconnect()

            if int(rtn['responseStatus']) == Define.SERVERDOWN:
                self.__serverdown = True'''
        finally:
            if not self.__th.isAlive():
                self.__th.start()

    def dht(self):

        tcpdht = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpdht.bind((self.__IP, 5000 + self.__ID))
        tcpdht.listen(2)

        path = os.getcwd()
        directory = os.path.join(path, 'DHT')
        if not os.path.exists(directory):
            os.makedirs(directory)

        while True:
            con, cliente = tcpdht.accept()
            msg = con.recv(1024)
            jsonmsg = json.loads(msg)

            if jsonmsg['type'] == Define.DHTFILES:
                array = jsonmsg['files']
                filepath = directory + '/' + jsonmsg['Hash']
                with open(filepath, 'wb') as f:
                    for index in range(len(array)):
                        rtn = self.__downloadserverhash(array[index])
                        jsonrtn = json.loads(rtn)
                        f.write(base64.b64decode(jsonrtn['data']))

            elif jsonmsg['type'] == Define.DOWNLOAD:
                filepath = directory + '/' + jsonmsg['Hash']
                with open(filepath, 'rb') as f:
                    data = f.read()
                    data64 = base64.b64encode(data)
                    msg = dict(responseStatus=Define.SUCCESS, type='file', data=data64)
                    con.send(json.dumps(msg))
