# coding=utf-8
import socket
import json
import base64
import Define


class ClientInterface:

    __IP = '192.168.200.179'   # Server IP
    __PORTSERVER = 5000  # Server PORT
    __PORTCLIENT = 4578  # Client PORT to recive DHT files
    __ID = 1            # ID do usuário

    def __init__(self):
        try:
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dest = (self.__IP, self.__PORTSERVER)
            #self.tcp.bind(('127.0.0.1', self.__PORTCLIENT))
            self.tcp.connect(dest)
        except socket.error as msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + str(msg[1])
            error = '{"code" : "' + str(Define.FAILEDCREATESOCK) + '", "msg" :  "Failed to create socket"}'
            jsonerror = json.loads(error)
            return jsonerror

    # Register a user
    # param: username - The username to register in database
    # return: json {code,msg}
    def __register(self, username):

        jsonmsg = dict(username=username, type=Define.REGISTER)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = jsonresponse["id"]
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=jsonresponse["responseStatus"], msg="Register Error")
            return error


    # Login a user
    # param: username - The username to login
    # return: json {code,msg}
    def login(self, username):

        jsonmsg = dict(username=username, type=Define.LOGIN)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = int(jsonresponse["id"])
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        elif int(jsonresponse["responseStatus"]) == Define.USERNOTREGISTER:
            return self.__register(username)
        else:
            error = dict(code=jsonresponse["responseStatus"], msg=jsonresponse["errormsg"])
            return error



    # Upload file to server
    # param: filename - Name of the file
    # param: data - Tho content of the file
    # param: path - The path of the file
    # return: json {code,msg}
    def upload(self, filename, data, path):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        datab64 = base64.b64encode(data)
        jsonmsg = dict(path=path, data=datab64, type=Define.UPLOAD)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Download file from server
    # param: path - The path of the file including file name
    # return: SUCCESS/ERROR CODE (if success file will be writen in a folder)
    def download(self, path):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(method='path', path=path, type=Define.DOWNLOAD)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            if jsonresponse["type"] == 'file':
                success = dict(code=Define.SUCCESS, msg=base64.b64decode(jsonresponse["data"]))
                return success
            elif jsonresponse["type"] == 'hash':
                jsonmsg = dict(method='hash', hash=str(jsonresponse["hashName"]), type=Define.DOWNLOAD)
                msg = json.dumps(jsonmsg)
                ip, port = jsonresponse["node"].split(':')
                response = self.__sendMSG(msg, ip, int(port))
                jsonresponse = json.loads(response)
                if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
                    success = dict(code=Define.SUCCESS, msg=base64.b64decode(jsonresponse["data"]))
                    return success
                else:
                    error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
                    return error
            else:
                error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
                return error

        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    def dirinfo(self):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(type=Define.DIRINFO)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg=str(jsonresponse["dir"]))
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Create directory
    # param: path - The path of the new directory without the new directory
    # param: namedir - The name of the new directory
    # return: SUCCESS/ERROR CODE
    def createdir(self, path, namedir):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(path=path, dirname=namedir, type=Define.CREATEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Rename directory
    # param: path - The path of the new directory included the directory to rename
    # param: namedir - The  new name of the directory
    # return: SUCCESS/ERROR CODE
    def renamedir(self, path, newnamedir):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(path=path, newname=newnamedir, type=Define.RENAMEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Remove directory
    # param: path - The path of the new directory included the directory to remove
    # return: SUCCESS/ERROR CODE
    def removedir(self, path):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(path=path, type=Define.REMOVEDIR)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Rename file
    # param: path - The path of the old file included the file to rename
    # param: namedir - The  new name of the file
    # return: SUCCESS/ERROR CODE
    def renamefile(self, path, newname):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(path=path, newname=newname, type=Define.RENAMEFILE)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    # Remove file
    # param: path - The path of the file included the file to remove
    # return: SUCCESS/ERROR CODE
    def removefile(self, path):
        if self.__ID == -1:
            error = dict(code=Define.USERUNAUTHENTICATED, msg="Permission denied, unauthenticated user")
            return error

        jsonmsg = dict(path=path, type=Define.REMOVEFILE)
        msg = json.dumps(jsonmsg)
        response = self.__sendMSGtoserver(msg)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = dict(code=Define.SUCCESS, msg='Success')
            return success
        else:
            error = dict(code=response["responseStatus"], msg=jsonresponse["errormsg"])
            return error

    def logout(self):
        self.tcp.close()

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
            error = '{"responseStatus" : "' + str(Define.SENDFAILED) + '", "errormsg" :  "Send Failed"}'
            return error

        rtn = con.recv(2048)
        con.close()

        return rtn

    def __sendMSGtoserver(self, msg):
        try:
            self.tcp.send(msg)
        except socket.error:
            # Send failed
            print 'Send failed'
            error = '{"responseStatus" : "' + str(Define.SENDFAILED) + '", "errormsg" :  "Send Failed"}'
            return error

        rtn = self.tcp.recv(2048)

        return rtn
