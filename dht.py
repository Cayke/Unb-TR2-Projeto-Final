from random import randint
import os
import json

class DHT (object):
    # Array responsavel por gerenciar os ids disponiveis.
    arrayWithEmptyIDs = [] # [ids]

    # Array responsavel por gerenciar os ids alocados.
    arrayWithAllocedIDs = [] # [(username, id)]

    # Array com os nos ativos
    arrayWithActiveNodes = [] # [(id,(ip,port))]

    workingPath = os.getcwd()
    maskWorkingPath = 'CFICloud'
    rootFolder = ''

    def __init__(self, k):
        for i in range(0, k):
            self.arrayWithEmptyIDs.append(i)

        self.createProgramPath()
       # dictionaryTreePath = self.getDirectoriesTreeForPath(self.rootFolder)
       # string = json.dumps(dictionaryTreePath)
       # print string

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

    def createProgramPath(self):
        self.rootFolder = os.path.join(self.workingPath, self.maskWorkingPath)
        if not os.path.exists(self.rootFolder):
            os.makedirs(self.rootFolder)

    # retorna um dicionario contendo {type: dir ou file, name: nome do mesmo, list: [dicts] contendo o que esta dentro dele
    #todo falta tirar o workingpath dos name = dirpath
    def getDirectoriesTreeForPath(self, path):
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
        return os.path.basename(fullPath)