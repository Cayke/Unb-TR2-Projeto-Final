import socket
import threading
import json
from dht import DHT
import Define

class MasterServer(object):
    HOST = ''
    PORT = 5000
    DHT = DHT(50)

    def __init__(self):
        print "servidor rodando..."
        self.waitForConnection()

    def waitForConnection(self):
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.HOST, self.PORT)
        socketTCP.bind(orig)
        socketTCP.listen(1)

        while True:
            con, client = socketTCP.accept()
            threading.Thread(target=self.clientConnected, args=(con,client)).start()

        socketTCP.close()

    def clientConnected(self, socketTCPThread, client):
        while True:
            try:
                #socketTCPThread.settimeout(60)
                data = socketTCPThread.recv(2048)
                request = json.loads(data)
                self.getRequestStatus(request,socketTCPThread,client)
            except socket.error as msg:
                print 'Error code: ' + str(msg[0]) + ', Error message: ' + str(msg[1])
                socketTCPThread.close()
                self.DHT.logOutUser(client)
                return False
            except:
                print 'ocorreu algum erro desconhecido, matando thread'
                return False

    def getRequestStatus(self, request, socketTCP, client):
        type = request['type']

        if type == Define.REGISTER:
            self.registerUser(request,socketTCP,client)

        elif type == Define.LOGIN:
            self.logUser(request,socketTCP,client)

        elif type == 'keepalive':
           self.userStillActive(request,socketTCP,client)

        elif type == Define.UPLOAD:
            self.uploadFile(request,socketTCP, client)

        elif type == Define.DOWNLOAD:
            self.downloadFile(request,socketTCP, client)

        elif type == Define.DIRINFO:
            self.sendDirectoriesTree(socketTCP)

        elif type == 'infofiles':
            self.infoFiles(request,socketTCP, client)

        elif type == Define.CREATEDIR:
            self.createDir(request,socketTCP, client)

        elif type == Define.RENAMEDIR:
            self.renameDir(request,socketTCP, client)

        elif type == Define.REMOVEDIR:
            self.removeDir(request,socketTCP, client)

        elif type == Define.REMOVEFILE:
            self.removeFile(request,socketTCP, client)

        elif type == Define.RENAMEFILE:
            self.renameFile(request,socketTCP, client)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'undefined_type')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def registerUser(self, request, socketTCP, client):
        username = request['username']
        id = self.DHT.registerUser(username, client)
        if id >= 0:
            response = dict(responseStatus = Define.SUCCESS, id = id)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)
            self.DHT.rebalancing()

        elif id == -1:
            response = dict(responseStatus = 'ERROR', errormsg = 'dht_overflow')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        elif id == -2:
            response = dict(responseStatus = 'ERROR', errormsg = 'user_already_registered')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def logUser(self, request, socketTCP, client):
        username = request['username']
        id = self.DHT.logUser(username, client)
        if id >= 0:
            response = dict(responseStatus = Define.SUCCESS, id = id)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)
            self.DHT.sendFilesToUser(id)

        elif id == -1:
            response = dict(responseStatus = Define.USERNOTREGISTER, errormsg = 'user_not_found')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def userStillActive(self, request, socketTCP, client):
        pass
        # if self.DHT.getIDForIPPort(client):
        #     response = dict(responseStatus = Define.SUCCESS)
        #     responseJSON = json.dumps(response)
        #     socketTCP.send(responseJSON)
        # else:
        #     response = dict(responseStatus = Define.USERUNAUTHENTICATED, message = 'you_are_not_logged')
        #     responseJSON = json.dumps(response)
        #     socketTCP.send(responseJSON)

    def uploadFile(self, request, socketTCP, client):
        path = str(request['path'])
        data = str(request['data'])

        if self.DHT.saveFileAtPath(path, data, client): #salvou
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def downloadFile(self, request, socketTCP, client):
        method = request['method']
        if method == 'hash':
            self.sendFileToUser(request,socketTCP,client)
        else:
            self.sendHostThatWillUpdloadFileToUser(request,socketTCP,client)

    def sendFileToUser(self, request, socketTCP, client):
        hash = request['hash']
        file = self.DHT.getBase64StringForFileWithHash(hash)
        response = dict(responseStatus = Define.SUCCESS, type = 'file', data = file)
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)

    def sendHostThatWillUpdloadFileToUser(self, request, socketTCP, client):
        path = request['path']
        hash = self.DHT.getHashForPath(path)
        id = self.DHT.getUserResponsableForFile(hash)

        if self.DHT.checkIfUserActive(id):
            response = dict(responseStatus = Define.SUCCESS, type = 'node', node = self.DHT.getIPPortForID(id), hashName = hash)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            request.update(hash = hash)
            self.sendFileToUser(request,socketTCP, client)

    def infoFiles(self, request,socketTCP, client):
        response = dict(responseStatus = Define.SUCCESS,
                        numberOfFiles = self.DHT.getNumberOfFiles,
                        capacityOfSystem = self.DHT.getCapacityOfSystem,
                        filesDistribution = self.DHT.getFilesDistribution,
                        activeNodes = self.DHT.getActiveNodes)
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)

    def createDir(self, request, socketTCP, client):
        path = request['path']

        if self.DHT.createDir(path,client):
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def renameDir(self, request, socketTCP, client):
        path = request['path']
        dir = request['newname']

        if self.DHT.renameDir(path,dir, client):
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def removeDir(self, request, socketTCP, client):
        path = request['path']

        if self.DHT.removeDir(path, client):
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def removeFile(self, request, socketTCP, client):
        path = request['path']

        if self.DHT.removeFile(path, client):
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def renameFile(self, request, socketTCP, client):
        path = request['path']
        newName = request['newname']

        if self.DHT.renameFile(path,newName, client):
            response = dict(responseStatus = Define.SUCCESS)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', errormsg = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    @staticmethod
    def sendFilesForUser(userID, ip, files):
        socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (ip, 5000 + userID)
        socketTCP.connect(dest)

        request = dict(type = 'dhtfiles', files = files)
        requestJSON = json.dumps(request)
        socketTCP.send(requestJSON)

    def sendDirectoriesTree(self, socketTCP):
        dictTree = self.DHT.getDirectioriesTree()
        response = dict(responseStatus = Define.SUCCESS, tree =[dictTree])
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)