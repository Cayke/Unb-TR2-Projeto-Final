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