import socket
import threading
import json
from dht import DHT

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
                data = socketTCPThread.recv(2048)
                request = json.loads(data)
                self.getRequestStatus(request,socketTCPThread,client)
            except:
                socketTCPThread.close()
                return False

    def getRequestStatus(self, request, socketTCP, client):
        type = request['type']

        if type == 'cadastro':
            self.registerUser(request,socketTCP,client)

        elif type == 'login':
            self.logUser(request,socketTCP,client)

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

        elif (id == -1):
            response = dict(responseStatus = 'ERROR', message = 'dht_overflow')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

        elif (id == -2):
            response = dict(responseStatus = 'ERROR', message = 'user_already_registered')
            responseJSON = json.dumps(response)
            socketTCP.send(responseJSON)

    def logUser(self, request, socketTCP, client):
        pass