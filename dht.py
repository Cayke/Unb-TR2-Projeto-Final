from random import randint
import os
import hashlib
import base64
import sys
import masterServer

class DHT (object):
    MAX_NODES = 0
    workingPath = os.getcwd()
    maskWorkingPath = 'CFICloud'
    rootFolder = ''

    # Array responsavel por gerenciar os ids disponiveis.
    arrayWithEmptyIDs = [] # [ids]

    # Array responsavel por gerenciar os ids alocados.
    arrayWithAllocedIDs = [] # [(username, id)]

    # Array com os nos ativos no momento
    arrayWithActiveNodes = [] # [(id,(ip,port))]

    # Array com os hashs dos arquivos salvos
    arrayWithHashAndPath = [] # [(path, hash)]

    # Array com ids e hashs
    arrayWithNodesResponsablesForHash = [] #[(id, hash)]


    def __init__(self, k):
        self.MAX_NODES = k
        for i in range(0, k):
            self.arrayWithEmptyIDs.append(i)

        self.createProgramPath()

        #self.test()

    def test(self):
        print self.getNumberOfFiles()
        print self.getCapacityOfSystem()
        print self.getFilesDistribution()

    def registerUser(self, username, client):
        if (self.checkIfUsernameAlreadyAlloced(username) == False):
            if len(self.arrayWithEmptyIDs) > 0:
                pos = randint(0, len(self.arrayWithEmptyIDs)-1)
                aloccedID = self.arrayWithEmptyIDs[pos]
                self.arrayWithEmptyIDs.remove(aloccedID)
                self.arrayWithAllocedIDs.append((username, aloccedID))
                self.arrayWithActiveNodes.append((aloccedID,client))
                self.createUserPath(username)
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

    def logOutUser(self, client):
        for (id, Client) in self.arrayWithActiveNodes:
            if client == Client:
                self.arrayWithActiveNodes.remove((id,client))
                break

    def getHashForPath(self, path):
        path = self.getLocalPathForPath(path)
        md5 = hashlib.md5()
        md5.update(path)
        return md5.hexdigest()

    def convertHashToInt(self, hash):
        value = 0
        for x in range(0, len(hash)):
            value += ord(hash[x])
        return value%self.MAX_NODES

    def getLocalPathForPath(self, path):
        root = self.getRootFromPath(path)
        if root == self.maskWorkingPath:
            path = path[1:]
            return os.path.join(self.workingPath, path)
        else:
            return path

    def getOutsidePathForPath(self, path):
        localPath = os.path.join(self.workingPath)
        return path.replace(localPath, '')

    def getRootFromPath(self, path):
        root = path
        root = root.lstrip(os.sep)
        return root[:root.index(os.sep)]

    def getFilePathForHash(self, hash):
        for (path, Hash) in self.arrayWithHashAndPath:
            if Hash == hash:
                return path
        return None

    def getUserResponsableForFile(self, hash):
        for (id, Hash) in self.arrayWithNodesResponsablesForHash:
            if Hash == hash:
                return id
        return -1

    def getBase64StringForFileWithHash(self, hash):
        path = self.getFilePathForHash(hash)
        with open(path, 'rb') as f:
            data = f.read()
            return base64.b64encode(data)

    def saveBase64ToPath(self, path, b64String):
        path = self.getLocalPathForPath(path)
        with open(path, 'wb') as f:
            data = base64.b64decode(b64String)
            f.write(data)
            return True
        return False

    def saveFileAtPath(self, path, file, client):
        path = self.getLocalPathForPath(path)
        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        path = self.getLocalPathForPath(path)
        if self.saveBase64ToPath(path, file):
            self.arrayWithHashAndPath.append((path,self.getHashForPath(path)))
            self.rebalancing()
            return True
        else:
            return False


    def checkIfUserActive(self, id):
        if self.getIPPortForID(id) != None:
            return True
        else:
            return False

    def getIPPortForID(self, id):
        for (ID, client) in self.arrayWithActiveNodes:
            if id == ID:
                return client
        return None

    def getIDForIPPort(self, client):
        for (id, Client) in self.arrayWithActiveNodes:
            if Client == client:
                return id
        return None

    def getUsernameForID(self, userID):
        for (username,id) in self.arrayWithAllocedIDs:
            if id == userID:
                return username
        return None

    def validateIfUserHasAccessToPath(self, path, client):
        removeLocal = os.path.join(self.workingPath, self.maskWorkingPath)
        removeLocal = path.replace(removeLocal, '')
        root = self.getRootFromPath(removeLocal)

        userID = self.getIDForIPPort(client)
        if self.getUsernameForID(userID) == root:
            return True
        else:
            return False

    def createDir(self, path, client):
        path = self.getLocalPathForPath(path)

        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        try:
            os.makedirs(path)
            return True
        except:
            return False

    def renameDir(self, path, newDirName, client):
        path = self.getLocalPathForPath(path)

        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        directory = os.path.dirname(path)
        newPath = os.path.join(directory, newDirName)
        try:
            os.rename(path, newPath)
            return True
        except:
            return False

    def removeDir(self, path, client):
        path = self.getLocalPathForPath(path)

        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
              os.rmdir(os.path.join(root, name))
        try:
            os.rmdir(path)
            return True
        except:
            return False

    def removeFile(self, path, client):
        path = self.getLocalPathForPath(path)

        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        try:
            os.remove(path)
            return True
        except:
            return False

    def renameFile(self, path, newFileName, client):
        path = self.getLocalPathForPath(path)

        if not self.validateIfUserHasAccessToPath(path, client):
            return False

        directory = os.path.dirname(path)
        newPath = os.path.join(directory, newFileName)
        try:
            os.rename(path, newPath)
            return True
        except:
            return False

    def createProgramPath(self):
        self.rootFolder = os.path.join(self.workingPath, self.maskWorkingPath)
        if not os.path.exists(self.rootFolder):
            os.makedirs(self.rootFolder)

    def createUserPath(self, username):
        userFolder = os.path.join(self.rootFolder, username)
        if not os.path.exists(userFolder):
            os.makedirs(userFolder)

    # retorna um dicionario contendo {type: dir ou file, name: nome do mesmo, list: [dicts] contendo o que esta dentro dele
    def getDirectioriesTree(self):
        return self.getDirectoriesTreeForPath(self.rootFolder)

    def getDirectoriesTreeForPath(self, path):
        path = self.getLocalPathForPath(path)
        for (dirpath, dirnames, filenames) in os.walk(path):
            try:
                filenames.remove('.DS_Store')
            except:
                pass

            if len(dirnames) == 0 and len(filenames) == 0:
                return dict(type = 'dir', name = self.getCurrentDirectoryName(dirpath), list = [])

            elif len(dirnames) == 0 and len(filenames) > 0:
                array = []
                for filename in filenames:
                    array.append(self.getDictionaryForFilename(filename))
                return dict(type = 'dir', name = self.getCurrentDirectoryName(dirpath), list = array)

            elif len(dirnames) > 0 and len(filenames) == 0:
                array = []
                for dirname in dirnames:
                    array.append(self.getDirectoriesTreeForPath(os.path.join(dirpath, dirname)))
                return dict(type = 'dir', name = self.getCurrentDirectoryName(dirpath), list = array)

            elif len(dirnames) > 0 and len(filenames) > 0:
                array = []
                for dirname in dirnames:
                    array.append(self.getDirectoriesTreeForPath(os.path.join(dirpath, dirname)))

                for filename in filenames:
                    array.append(self.getDictionaryForFilename(filename))
                return dict(type = 'dir', name = self.getCurrentDirectoryName(dirpath), list = array)


    def getDictionaryForFilename(self, filename):
        return dict(type = 'file', name = filename)

    def getCurrentDirectoryName(self, fullPath):
        fullPath = self.getLocalPathForPath(fullPath)
        return os.path.basename(fullPath)

    def rebalancing(self):
        self.arrayWithNodesResponsablesForHash = []
        for (path,hash) in self.arrayWithHashAndPath:
            fileID = self.convertHashToInt(hash)
            node = self.responsableNodeForFileID(fileID)
            self.arrayWithNodesResponsablesForHash.append((node, hash))
        self.sendHashsToAllNodes()

    def responsableNodeForFileID(self, fileID):
        # Array responsavel por gerenciar os ids alocados.
        # arrayWithAllocedIDs = [] # [(username, id)]
        responsableNode = sys.maxint
        minNodeValue = sys.maxint
        for (username, nodeID) in self.arrayWithAllocedIDs:
            if nodeID == fileID:
                return nodeID
            elif nodeID > fileID and nodeID < responsableNode:
                responsableNode = nodeID
            elif nodeID < minNodeValue:
                minNodeValue = nodeID

        if responsableNode == sys.maxint:
            return minNodeValue
        else:
            return responsableNode


    def sendHashsToAllNodes(self):
        for (id, client) in self.arrayWithActiveNodes:
            self.sendFilesToUser(id)

    def getListWithHashesForUserID(self, userID):
        array = []
        for (id,hash) in self.arrayWithNodesResponsablesForHash:
            if id == userID:
                array.append(hash)
        return array

    def sendFilesToUser(self, userID):
        (ip, port) = self.getIPPortForID(userID)
        listWithHashes = self.getListWithHashesForUserID(userID)
        masterServer.MasterServer.sendFilesForUser(userID, ip, listWithHashes)

    #retorna numero de arquivos
    def getNumberOfFiles(self):
        numberOfFiles = 0
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.workingPath, self.maskWorkingPath)):
            try:
                filenames.remove('.DS_Store')
            except:
                pass
            numberOfFiles = numberOfFiles + len(filenames)
        return numberOfFiles

    #retorna tamanho em bytes
    def getCapacityOfSystem(self):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(os.path.join(self.workingPath, self.maskWorkingPath)):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def getFilesDistribution(self):
        array = []
        for (path, hash) in self.arrayWithHashAndPath:
            userID = self.getUserResponsableForFile(hash)
            username = self.getUsernameForID(userID)
            outPath = self.getOutsidePathForPath(path)
            array.append(dict(file = outPath, username = username))
        return array

    def getActiveNodes(self):
        array = []
        for (id, client) in self.arrayWithActiveNodes:
            array.append(self.getUsernameForID(id))
        return array