import socket
import threading
import json
from dht import DHT

class MasterServer(object):
    HOST = ''
    PORT = 50005
    DHT = DHT(50)

    def __init__(self):
        self.DHT.MasterServer = self
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
                socketTCPThread.settimeout(30)
                data = socketTCPThread.recv(2048)
                request = json.loads(data)
                self.getRequestStatus(request,socketTCPThread,client)
            except:
                socketTCPThread.close()
                self.DHT.logOutUser(client)
                return False

    def getRequestStatus(self, request, socketTCP, client):
        type = request['type']

        if type == 'cadastro':
            self.registerUser(request,socketTCP,client)

        elif type == 'login':
            self.logUser(request,socketTCP,client)

        elif type == 'keepalive':
           self.userStillActive(request,socketTCP,client)

        elif type == 'upload':
            self.uploadFile(request,socketTCP, client)

        elif type == 'download':
            self.downloadFile(request,socketTCP, client)

        elif type == 'dirinfo':
            self.sendDirectoriesTree(socketTCP)

        elif type == 'infofiles':
            self.infoFiles(request,socketTCP, client)

        elif type == 'createdir':
            self.createDir(request,socketTCP, client)

        elif type == 'renamedir':
            self.renameDir(request,socketTCP, client)

        elif type == 'removedir':
            self.removeDir(request,socketTCP, client)

        elif type == 'removefile':
            self.removeFile(request,socketTCP, client)

        elif type == 'renamefile':
            self.renameFile(request,socketTCP, client)

        else:
            response = dict(responseStatus = 'ERROR', message = 'undefined_type')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def registerUser(self, request, socketTCP, client):
        username = request['username']
        id = self.DHT.registerUser(username, client)
        if (id >= 0):
            response = dict(responseStatus = 'SUCCESS', id = id)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)
            self.DHT.rebalancing()

        elif (id == -1):
            response = dict(responseStatus = 'ERROR', message = 'dht_overflow')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        elif (id == -2):
            response = dict(responseStatus = 'ERROR', message = 'user_already_registered')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def logUser(self, request, socketTCP, client):
        username = request['username']
        id = self.DHT.logUser(username, client)
        if (id >= 0):
            response = dict(responseStatus = 'SUCCESS', id = id)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        elif (id == -1):
            response = dict(responseStatus = 'ERROR', message = 'user_not_found')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def userStillActive(self, request, socketTCP, client):
        if self.DHT.getIDForIPPort(client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)
        else:
            response = dict(responseStatus = 'ERROR', message = 'you_are_not_logged')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def uploadFile(self, request, socketTCP, client):
        path = request['path']
        data = request['data']

        if(self.DHT.saveFileAtPath(path, data, client)): #salvou
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
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
        response = dict(responseStatus = 'SUCCESS', type = 'file', data = file)
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)

    def sendHostThatWillUpdloadFileToUser(self, request, socketTCP, client):
        path = request['path']
        hash = self.DHT.getHashForPath(path)
        id = self.DHT.getUserResponsableForFile(hash)

        if self.DHT.checkIfUserActive(id):
            response = dict(responseStatus = 'SUCCESS', type = 'node', node = self.DHT.getIPPortForID(id), hashName = hash)
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            request.update(hash = hash)
            self.sendFileToUser(request,socketTCP, client)

    def infoFiles(self, request,socketTCP, client):
        response = dict(responseStatus = 'SUCCESS',
                        numberOfFiles = self.DHT.getNumberOfFiles,
                        capacityOfSystem = self.DHT.getCapacityOfSystem,
                        filesDistribution = self.DHT.getFilesDistribution,
                        activeNodes = self.DHT.getActiveNodes)
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)

    def createDir(self, request, socketTCP, client):
        path = request['path']
        dir = request['dirname']

        if self.DHT.createDir(path,dir,client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def renameDir(self, request, socketTCP, client):
        path = request['path']
        dir = request['newname']

        if self.DHT.renameDir(path,dir, client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def removeDir(self, request, socketTCP, client):
        path = request['path']

        if self.DHT.removeDir(path, client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def removeFile(self, request, socketTCP, client):
        path = request['path']

        if self.DHT.removeFile(path, client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def renameFile(self, request, socketTCP, client):
        path = request['path']
        newName = request['newname']

        if self.DHT.renameFile(path,newName, client):
            response = dict(responseStatus = 'SUCCESS')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        else:
            response = dict(responseStatus = 'ERROR', message = 'error_processing_file')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def sendFilesForUser(self, socketTCP, files):
        response = dict(type = 'dhtfiles', files = files)
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)

    def sendDirectoriesTree(self, socketTCP):
        dictTree = self.DHT.getDirectioriesTree()
        response = [dictTree]
        responseJSON = json.dumps(response)
        socketTCP.send(responseJSON)