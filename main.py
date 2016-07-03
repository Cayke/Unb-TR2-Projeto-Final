from tempfile import TemporaryFile
from wsgiref.util import setup_testing_defaults
from wsgiref import simple_server
import cgi, re
from ServerRequests import *
import UIGenerator
import json

class UIServer:

    STATIC_URL_PREFIX = '/static/'
    STATIC_FILE_DIR = 'static/'     
    userName = ""
    server = None
    urls = []
    serverRequests = None

    def __init__(self):
        self.urls = [(r'^$',self.main),
            (r'login/?$',self.login),
            (r'uploadFile/?$',self.uploadFile),
            (r'dirPage/serverInfo/?$',self.serverInfo),
            (r'filesStructure/?$',self.fileStructure),
            (r'filePage/?(.*)',self.filePage),
            (r'dirPage/?(.*)',self.dirPage),
            (r'donwload/?(.*)',self.downloadFile)]
        print "Listening on port 8000...."
        self.serverRequests = ServerRequests()
        print "here"
        server=simple_server.make_server('', 8000, self.app)
        server.serve_forever()


#MARK: Error
    def not_found(self,environ, start_response):
        """Called if no URL matches."""
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return ['Not Found']

#MARK: Login
    def main(self,env,resp):
        resp('200 OK', [('Content-type', 'text/html')])
        login = open('templates/login.html','r').read()
        if env['REQUEST_METHOD'] == 'POST':
            post_env = env.copy()
            post_env['QUERY_STRING'] = ''
            post = cgi.FieldStorage(
                fp=env['wsgi.input'],
                environ=post_env,
                keep_blank_values=True
            )
            self.userName = post["user"]
            print self.userName
        else:
            return [login]

    def login(self,env,resp):
        if env['REQUEST_METHOD'] == 'POST':
            post_env = env.copy()
            post_env['QUERY_STRING'] = ''
            post = cgi.FieldStorage(
                fp=env['wsgi.input'],
                environ=post_env,
                keep_blank_values=True
            )
            self.userName = post['user'].value
            if (self.serverRequests.login(self.userName)):
                return self.fileStructure(env,resp)
            else:
                return self.errorScreen(env,resp)
        return [self.userName]

#MARK: Files page
    def fileStructure(self,env,resp):
        jsonFile = self.serverRequests.fileDistribution()
        if (jsonFile == None):
            return self.errorScreen(env,resp)
        html = UIGenerator.generateFileTreePage(jsonFile)
        resp('200 OK', [('Content-type', 'text/html')])
        return html

#MARK: Dir operations
    def dirPage(self,env,resp):
        dirPage = open('templates/dirPage.html','r').read()
        dirPage = dirPage.replace("#PATH#",env['PATH_INFO']) 
        dirName = dirPage.split('/')[-1]
        query_string = env['QUERY_STRING']
        action = query_string.split('=')[-1]
        if action == "Delete":
            if self.serverRequests.removeFile(dirName,dirPage):
                return self.fileStructure(env,resp)
            else:
                return self.errorScreen(env,resp)
        resp('200 OK', [('Content-type', 'text/html')])
        return [dirPage]

    def uploadFile(self,env,resp):
        print "Here"
        body = self.readUploadFile(env)
        form = cgi.FieldStorage(fp=body, environ=env, keep_blank_values=True)
        print form
        return self.fileStructure(env,resp)
    
    def readUploadFile(self,env):
        length = int(env.get('CONTENT_LENGTH', 0))
        stream = env['wsgi.input']
        body = TemporaryFile(mode='w+b')
        while length > 0:
            part = stream.read(min(length, 1024*200)) # 200KB buffer size
            if not part: break
            body.write(part)
            length -= len(part)
        body.seek(0)
        env['wsgi.input'] = body
        return body

#MARK: FILES OPERATIOS
    def filePage(self,env,resp):
        filePage = open('templates/filePage.html','r').read()
        filePath = env['PATH_INFO'].strip("/filePage")
        fileName = filePath.split('/')[-1]
        filePage = filePage.replace("#PATH#",filePath) 
        filePage = filePage.replace("#FILE#",fileName)
        query_string = env['QUERY_STRING']
        action = query_string.split('=')[-1]
        if action == "Download":
            return self.downloadFile(filePath,resp)
        elif action == "Delete":
            if self.serverRequests.removeFile(fileName,filePath):
                return self.fileStructure(env,resp)
            else:
                return self.errorScreen(env,resp)
        resp('200 OK', [('Content-type', 'text/html')])
        return [filePage]

    def downloadFile(self,filePath, resp):
        file = self.serverRequests.downloadFile(filePath)
        if (file == None):
            return self.errorScreen(env,resp)
        resp('200 OK', [('Content-type', 'text/pain')])
        return [file]

#MARK: Server info
    def serverInfo(self,env,resp):
        info = self.serverRequests.getServerInfo()
        if (info == None):
            return self.errorScreen(env,resp)
        resp('200 OK', [('Content-type', 'text/pain')])
        return [info]

#MARK: Static folder reading
    def static_app(self,env, resp):
        """Serve static files from the directory named
        in STATIC_FILES"""
        path = env['PATH_INFO']
        # we want to remove '/static' from the start
        path = path.replace(self.STATIC_URL_PREFIX, self.STATIC_FILE_DIR)
        h = open(path, 'rb')
        content = h.read()
        h.close()
        headers = [('content-type', 'text/plain')]
        resp('200 OK', headers)
        return [content]    

#MARK: Main manager        
    def app(self,env, resp):
        if env['PATH_INFO'].startswith(self.STATIC_URL_PREFIX):
            return self.static_app(env, resp)
        else:
            path = env.get('PATH_INFO', '').lstrip('/')
            print path
            for regex, callback in self.urls:
                match = re.search(regex, path)
                if match is not None:
                    env['myapp.url_args'] = match.groups()
                    return callback(env, resp)
            
        return self.not_found(env, resp)
    def errorScreen(self,env, resp):
        resp('200 OK', [('Content-type', 'text/pain')])
        return ['The request failed. Please go back and try again.']

UIServer()    