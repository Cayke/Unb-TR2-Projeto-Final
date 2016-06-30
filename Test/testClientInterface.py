import unittest
import json
import base64
import unicodedata
import sys
sys.path.insert(0, '/home/igor/Projetos/tr2-trabalhofinal')
from ClientInterface import ClientInterface
import Define

class TestClientMethods(unittest.TestCase):

    '''def test_login_success(self):
        client = ClientInterface()
        rtn = client.login('test')
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)
        self.assertEquals(rtnjson["msg"], 'Success')'''

    def test_registerlogin_success(self):
        client = ClientInterface()
        rtn = client.login('test')
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)
        self.assertEquals(rtnjson["msg"], 'Success')

    def test_upload_success(self):
        client = ClientInterface()
        datab64 = base64.b64encode('abcdefghijklmnopqrstuwxyz')
        rtn = client.upload('test.txt', datab64, '/')
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)
        self.assertEquals(rtnjson["msg"], 'Success')

    def test_downloadfile_success(self):
        client = ClientInterface()
        rtn = client.download('/')
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)
        self.assertEquals(rtnjson["msg"], 'abcdefghijklmnopqrstuwxyz')

    def test_dirinfo_success(self):
        client = ClientInterface()
        rtn = client.dirinfo()
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)


if __name__ == '__main__':
    unittest.main()



