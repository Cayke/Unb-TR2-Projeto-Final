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

    def test_registerlogin_success(self):
        rtn = client.login('test')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'Success')

    @unittest.skip("demonstrating skipping")
    def test_upload_success(self):
        datab64 = base64.b64encode('abcdefghijklmnopqrstuwxyz')
        rtn = client.upload('test.txt', datab64, '/')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'Success')

    @unittest.skip("demonstrating skipping")
    def test_downloadfile_success(self):
        rtn = client.download('/')
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'abcdefghijklmnopqrstuwxyz')

    @unittest.skip("demonstrating skipping")
    def test_dirinfo_success(self):
        rtn = client.dirinfo()
        # rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "/")

    @unittest.skip("demonstrating skipping")
    def test_createdir_success(self):
        rtn = client.createdir('/', "test")
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")
    def test_renamedir_success(self):
        rtn = client.renamedir('/', "test")
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")
    def test_removedir_success(self):
        rtn = client.removedir('/')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")
    def test_renamefile_success(self):
        rtn = client.renamefile('/', 'test')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    @unittest.skip("demonstrating skipping")
    def test_removefile_success(self):
        rtn = client.removefile('/')
        #rtnjson = json.loads(rtn)
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")


if __name__ == '__main__':
    unittest.main()



