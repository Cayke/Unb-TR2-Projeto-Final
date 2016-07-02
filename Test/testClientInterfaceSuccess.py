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


    @unittest.skip("demonstrating skipping")
    def test_login_success(self):
        rtn = client.login('test')
        rtnjson = json.loads(rtn)
        self.assertEqual(int(rtnjson["code"]), Define.SUCCESS)
        self.assertEquals(rtnjson["msg"], 'Success')


    #unittest.skip("demonstrating skipping")#PASS
    def test_registerlogin_success(self):
        rtn = client.login('test')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'Success')

    @unittest.skip("demonstrating skipping")#PASS
    def test_upload_success(self):
        rtn = client.upload('abcdefghijklmnopqrstuwxyz', '/CFICloud/test/test.txt')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'Success')

    @unittest.skip("demonstrating skipping")#pass
    def test_downloadfile_success(self):
        client.login('test')
        client.upload('abcdefghijklmnopqrstuwxyz', '/CFICloud/test/test.txt')
        rtn = client.download('/CFICloud/test/test.txt')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'abcdefghijklmnopqrstuwxyz')

    @unittest.skip("demonstrating skipping")#PASS
    def test_dirinfo_success(self):
        rtn = client.dirinfo()
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        #self.assertEqual(rtn["msg"], "/")

    @unittest.skip("demonstrating skipping")#PASS
    def test_createdir_success(self):
        client.login('test')
        rtn = client.createdir('/CFICloud/test/', "1")
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")#pass
    def test_renamedir_success(self):
        client.login('test')
        rtn = client.renamedir('/CFICloud/test/abc/', "def")
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")#PASS
    def test_removedir_success(self):
        client.login('test')
        rtn = client.removedir('/CFICloud/test/def/')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")#PASS
    def test_renamefile_success(self):
        client.login('test')
        rtn = client.renamefile('/CFICloud/test/test.txt', 'test2.txt')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")#pass
    def test_removefile_success(self):
        client.login('test')
        rtn = client.removefile('/CFICloud/test/test2.txt')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")


if __name__ == '__main__':
    unittest.main()



