from random import randint

class DHT (object):
    # Array responsavel por gerenciar os ids disponiveis.
    arrayWithEmptyIDs = [] # [ids]

    # Array responsavel por gerenciar os ids alocados.
    arrayWithAllocedIDs = [] # [(username, id)]

    # Array com os nos ativos
    arrayWithActiveNodes = [] # [(id,(ip,port))]



    def __init__(self, k):
        for i in range(0, k):
            self.arrayWithEmptyIDs.append(i)

    def registerUser(self, username, client):
        if (self.checkIfUsernameAlreadyAlloced(username) == False):
            if len(self.arrayWithEmptyIDs) > 0:
                pos = randint(0, len(self.arrayWithEmptyIDs)-1)
                aloccedID = self.arrayWithEmptyIDs[pos]
                self.arrayWithEmptyIDs.remove(aloccedID)
                self.arrayWithAllocedIDs.append((username, aloccedID))
                self.arrayWithActiveNodes.append((aloccedID,client))
                return aloccedID
            else:
                return -1
        else:
            return -2

    def checkIfUsernameAlreadyAlloced(self, username):
        for (uName, id) in self.arrayWithAllocedIDs:
            if (username == uName):
                return True
        return False

    def logUser(self, username, client):
        for (uName, id) in self.arrayWithAllocedIDs:
            if (username == uName):
                self.arrayWithActiveNodes.append((id, client))
                return id
        return -1

    def getHashForPath(self, path):
        #todo
        return ''

    def getUserResponsableForFile(self, hash):
        #todo ver usuario responsavel pelo hash
        return 0

    def getBase64StringForFileWithHash(self, hash):
        #todo get file with hash
        return ''

    def checkIfUserActive(self, id):
        # todo ver se usuario ativo
        return True

    def getIPPortForID(self, id):
        # todo pegar ip porta
        return ('localhost', 5000)

    def createDir(self, path, dirName):
        # todo
        return True

    def renameDir(self, path, newDirName):
        # todo
        return True

    def removeDir(self, path):
        # todo
        return True

    def removeFile(self, path):
        # todo
        return True

    def renameFile(self, path, newFileName):
        # todo
        return True