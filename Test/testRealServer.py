import unittest
import time
import sys
sys.path.insert(0, '/home/igor/Projetos/tr2-trabalhofinal')
from ClientInterface import ClientInterface
import Define





class TestClientMethods(unittest.TestCase):

    def test_success(self):
        client = ClientInterface()
        #login
        rtn = client.login('test')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'Success')
        #createdir
        #time.sleep(60)
        rtn = client.createdir('/CFICloud/test/', "1")
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        #renamedir
        rtn = client.renamedir('/CFICloud/test/1', "def")
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        #upload
        rtn = client.upload('abcdefghijklmnopqrstuwxyz', '/CFICloud/test/test.txt')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        #download
        rtn = client.download('/CFICloud/test/test.txt')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEquals(rtn["msg"], 'abcdefghijklmnopqrstuwxyz')
        #removedir
        rtn = client.removedir('/CFICloud/test/1/')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        #renamefile
        rtn = client.renamefile('/CFICloud/test/test.txt', 'test2.txt')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")
        #removefile
        #time.sleep(60)
        rtn = client.removefile('/CFICloud/test/test2.txt')
        self.assertEqual(int(rtn["code"]), Define.SUCCESS)
        self.assertEqual(rtn["msg"], "Success")

    '''@unittest.skip("demonstrating skipping")
    def test_renamedir_failed(self):
        rtn = client.renamedir('/CFICloud/test/1', "2")
        #self.assertEqual(int(rtn["code"]), Define.)

    @unittest.skip("demonstrating skipping")
    def test_removedir_failed(self):
        rtn = client.removedir('/CFICloud/test/def/')
        #self.assertEqual(int(rtn["code"]), Define.)


    @unittest.skip("demonstrating skipping")
    def test_upload_failed(self):
        rtn = client.upload('abcdefghijklmnopqrstuwxyz', '/CFICloud/test/fail/test.txt')
        #self.assertEqual(int(rtn["code"]), Define.)


    @unittest.skip("demonstrating skipping")
    def test_download_failed(self):
        rtn = client.download('/CFICloud/test/fail/test.txt')
        #self.assertEqual(int(rtn["code"]), Define.)

    @unittest.skip("demonstrating skipping")
    def test_renamefile_success(self):
        client.login('test')
        rtn = client.renamefile('/CFICloud/test/test6.txt', 'test2.txt')
        #self.assertEqual(int(rtn["code"]), Define.)

    @unittest.skip("demonstrating skipping")
    def test_removefile_failed(self):
        client.login('test')
        rtn = client.removefile('/CFICloud/test/test3.txt')
        #self.assertEqual(int(rtn["code"]), Define.)

    @unittest.skip("demonstrating skipping")
    def test_removefile_failed2(self):
        client.login('test')
        rtn = client.removefile('/CFICloud/test/failed/test2.txt')
        #self.assertEqual(int(rtn["code"]), Define.)'''


if __name__ == '__main__':
    unittest.main()



