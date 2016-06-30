# coding=utf-8
import socket
import json
import base64
import Define


class ClientInterface:

    __IP = '127.0.0.1'   # Server IP
    __PORTSERVER = 3301  # Server PORT
    __PORTCLIENT = 4578  # Client PORT to recive DHT files
    __ID = 1            # ID do usuário

    def __init__(self):
        pass

    # Register a user
    # param: username - The username to register in database
    # return: json {code,msg}
    def __register(self, username):
        msg = '{"username" : "' + username + '", "type" : ' + str(Define.REGISTER) + ' }'

        response = self.__sendMSG(msg, self.__IP, self.__PORTSERVER)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = jsonresponse["id"]
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            return success
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Register Error"}'
            jsonerror = json.loads(error)
            return jsonerror


    # Login a user
    # param: username - The username to login
    # return: json {code,msg}
    def login(self, username):
        msg = '{"username" : "' + username + '", "type" : ' + str(Define.LOGIN) + ' }'

        response = self.__sendMSG(msg, self.__IP, self.__PORTSERVER)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            self.__ID = int(jsonresponse["id"])
            success = '{"code" : ' + str(Define.SUCCESS) + ', "msg" :  "Success"}'
            return success
        elif int(jsonresponse["responseStatus"]) == Define.USERNOTREGISTER:
            return self.__register(username)
        else:
            error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Login Error"}'
            return error



    # Upload file to server
    # param: filename - Name of the file
    # param: data - Tho content of the file
    # param: path - The path of the file
    # return: json {code,msg}
    def upload(self, filename, data, path):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            return error

        datab64 = base64.b64encode(data)
        msg = '{"path" : "' + path + '", "data" : "' + datab64 + '", "type" : ' + str(Define.UPLOAD) + ' }'

        response = self.__sendMSG(msg, self.__IP, self.__PORTSERVER)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            return success
        else:
            error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Upload Error"}'
            return error

    # Download file from server
    # param: path - The path of the file including file name
    # return: SUCCESS/ERROR CODE (if success file will be writen in a folder)
    def download(self, path):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            return error

        msg = '{"type" : ' + str(Define.DOWNLOAD) + ', "method" : "path", "path" : "' + path + '" }'

        response = self.__sendMSG(msg, self.__IP, self.__PORTSERVER)
        jsonresponse = json.loads(response)

        if int(jsonresponse["responseStatus"]) == Define.SUCCESS:
            if jsonresponse["type"] == 'file':
                success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "' + base64.b64decode(jsonresponse["data"]) + '"}'
                return success
            elif response["type"] == 'hash':
                msg = '{"type" : ' + str(Define.DOWNLOAD) + ', "method" : "hash", "hash" : "' + response["hashName"] + '" }'
                jsonmsg = json.loads(msg)
                ip, port = response["node"].split(':')
                response = self.__sendMSG(jsonmsg, ip, port)
                jsonresponse = json.loads(response)
                if jsonresponse["responseStatus"] == Define.SUCCESS:
                    success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "' + base64.b64decode(jsonresponse["data"]) + '"}'
                    return success
                else:
                    error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Download Error"}'
                    return error
            else:
                error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Download Error"}'
                return error

        else:
            error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Download Error"}'
            return error

    def dirinfo(self):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            return error

        msg = '{"type" : ' + str(Define.DIRINFO) + ' }'

        response = self.__sendMSG(msg, self.__IP, self.__PORTSERVER)
        jsonresponse = json.loads(response)

        if jsonresponse["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" : "' + jsonresponse["dir"] + '"}'
            return success
        else:
            error = '{"code" : "' + jsonresponse["responseStatus"] + '", "msg" :  "Upload Error"}'
            return error

    # Create directory
    # param: path - The path of the new directory without the new directory
    # param: namedir - The name of the new directory
    # return: SUCCESS/ERROR CODE
    def createdir(self, path, namedir):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            jsonerror = json.loads(error)
            return jsonerror

        msg = '{"path" : ' + path + ', "dirname" : "' + namedir + '", "type" : ' + Define.CREATEDIR + ' }'
        jsonmsg = json.loads(msg)

        response = self.__sendMSG(jsonmsg, self.__IP, self.__PORTSERVER)

        if response["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            jsonsuccess = json.loads(success)
            return jsonsuccess
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Upload Error"}'
            jsonerror = json.loads(error)
            return jsonerror

    # Rename directory
    # param: path - The path of the new directory included the directory to rename
    # param: namedir - The  new name of the directory
    # return: SUCCESS/ERROR CODE
    def renamedir(self, path, namedir):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            jsonerror = json.loads(error)
            return jsonerror

        msg = '{"path" : ' + path + ', "newname" : "' + namedir + '", "type" : ' + Define.RENAMEDIR + ' }'
        jsonmsg = json.loads(msg)

        response = self.__sendMSG(jsonmsg, self.__IP, self.__PORTSERVER)

        if response["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            jsonsuccess = json.loads(success)
            return jsonsuccess
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Upload Error"}'
            jsonerror = json.loads(error)
            return jsonerror

    # Remove directory
    # param: path - The path of the new directory included the directory to remove
    # return: SUCCESS/ERROR CODE
    def removedir(self, path):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            jsonerror = json.loads(error)
            return jsonerror

        msg = '{"path" : ' + path + '", "type" : ' + Define.REMOVEDIR + ' }'
        jsonmsg = json.loads(msg)

        response = self.__sendMSG(jsonmsg, self.__IP, self.__PORTSERVER)

        if response["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            jsonsuccess = json.loads(success)
            return jsonsuccess
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Upload Error"}'
            jsonerror = json.loads(error)
            return jsonerror

    # Rename file
    # param: path - The path of the old file included the file to rename
    # param: namedir - The  new name of the file
    # return: SUCCESS/ERROR CODE
    def renamefile(self, path, newname):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            jsonerror = json.loads(error)
            return jsonerror

        msg = '{"path" : ' + path + ', "newname" : "' + newname + '", "type" : ' + str(Define.RENAMEFILE) + ' }'
        jsonmsg = json.loads(msg)

        response = self.__sendMSG(jsonmsg, self.__IP, self.__PORTSERVER)

        if response["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            jsonsuccess = json.loads(success)
            return jsonsuccess
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Upload Error"}'
            jsonerror = json.loads(error)
            return jsonerror

    # Remove file
    # param: path - The path of the file included the file to remove
    # return: SUCCESS/ERROR CODE
    def removefile(self, path):
        if self.__ID == -1:
            error = '{"code" : "' + str(Define.USERUNAUTHENTICATED) + '", "msg" :  "Permission denied, unauthenticated user"}'
            jsonerror = json.loads(error)
            return jsonerror

        msg = '{"path" : ' + path + '", "type" : ' + str(Define.REMOVEFILE) + ' }'
        jsonmsg = json.loads(msg)

        response = self.__sendMSG(jsonmsg, self.__IP, self.__PORTSERVER)

        if response["responseStatus"] == Define.SUCCESS:
            success = '{"code" : "' + str(Define.SUCCESS) + '", "msg" :  "Success"}'
            jsonsuccess = json.loads(success)
            return jsonsuccess
        else:
            error = '{"code" : "' + response["responseStatus"] + '", "msg" :  "Upload Error"}'
            jsonerror = json.loads(error)
            return jsonerror

    def __sendMSG(self, msg, ip, port):
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + str(msg[1])
            error = '{"code" : "' + str(Define.FAILEDCREATESOCK) + '", "msg" :  "Failed to create socket"}'
            jsonerror = json.loads(error)
            return jsonerror

        dest = (ip, port)
        tcp.connect(dest)

        try:
            tcp.send(msg)
        except socket.error:
            # Send failed
            print 'Send failed'
            error = '{"code" : "' + str(Define.FAILEDCREATESOCK) + '", "msg" :  "Send failed"}'
            jsonerror = json.loads(error)
            return jsonerror

        rtn = tcp.recv(512)
        tcp.close()

        return rtn
