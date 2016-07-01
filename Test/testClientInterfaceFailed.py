import unittest
import json
import base64
import unicodedata
import sys
sys.path.insert(0, '/home/igor/Projetos/tr2-trabalhofinal')
from ClientInterface import ClientInterface
import Define


client = ClientInterface()


class TestClientMethods(unittest.TestCase):

    def test_tcpsocket_failed(self):
        rtn = client.login('test')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SENDFAILED)
        self.assertEquals(rtn["msg"], 'Send Failed')

    def test_authenticated_failed(self):
        rtn = client.dirinfo()
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.USERUNAUTHENTICATED)
        self.assertEquals(rtn["msg"], 'Permission denied, unauthenticated user')
        client.logout()

if __name__ == '__main__':
    unittest.main()



