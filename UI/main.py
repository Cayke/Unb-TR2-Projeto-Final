from wsgiref.util import setup_testing_defaults
from wsgiref import simple_server
import cgi
import re
import getServerRequests
import UIGenerator
import json

class UIServer:

    STATIC_URL_PREFIX = '/static/'
    STATIC_FILE_DIR = 'static/'     
    userName = ""
    server = None
    urls = []
    def __init__(self):
        self.urls = [(r'^$',self.main),
            (r'login/?$',self.login),
            (r'filesStructure/?$',self.fileStructure),
            (r'filePage/?(.*)',self.filePage),
            (r'dirPage/?(.*)',self.dirPage),
            (r'donwload/?(.*)',self.downloadFile)]
        print "Listening on port 8000...."
        server=simple_server.make_server('', 8000, self.app)
        server.serve_forever()

    def not_found(self,environ, start_response):
        """Called if no URL matches."""
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return ['Not Found']

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
            return self.fileStructure(env,resp)
        return [self.userName]

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

    def fileStructure(self,env,resp):
        resp('200 OK', [('Content-type', 'text/html')])
        jsonFile = getServerRequests.fileDistribution()
        html = UIGenerator.generateFileTreePage(jsonFile)
        return [html]

    def filePage(self,env,resp):
        resp('200 OK', [('Content-type', 'text/html')])
        filePage = open('templates/filePage.html','r').read()
        filePage = filePage.replace("#PATH#",env['PATH_INFO']) 
        return [filePage]

    def dirPage(self,env,resp):
        resp('200 OK', [('Content-type', 'text/html')])
        dirPage = open('templates/dirPage.html','r').read()
        dirPage = dirPage.replace("#PATH#",env['PATH_INFO']) 
        return [dirPage]

    def downloadFile(self,env,resp):
        file = getServerRequests.downloadFile()
# TODO: Present file

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

    # A relatively simple WSGI application. It's going to print out the
    # environment dictionary after being updated by setup_testing_defaults
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

UIServer()    