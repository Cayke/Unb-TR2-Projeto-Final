from wsgiref.util import setup_testing_defaults
from wsgiref import simple_server
import cgi
import re
import UIGenerator
import json

def not_found(environ, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

def login(env,resp):
    resp('200 OK', [('Content-type', 'text/html')])
    login = open('templates/login.html','r').read()
    # if env['REQUEST_METHOD'] == 'POST':
    #     post_env = env.copy()
    #     post_env['QUERY_STRING'] = ''
    #     post = cgi.FieldStorage(
    #         fp=env['wsgi.input'],
    #         environ=post_env,
    #         keep_blank_values=True
    #     )
    #     with open('templates/test.json') as data_file: 
    #         jsonFile = json.load(data_file)
    #     login = UIGenerator.generateFileTreePage(jsonFile)
    return [login]

def fileStructure(env,resp):
    resp('200 OK', [('Content-type', 'text/html')])
    with open('templates/test.json') as data_file: 
            jsonFile = json.load(data_file)
    html = UIGenerator.generateFileTreePage(jsonFile)
    return [html]

def filePage(env,resp):
    resp('200 OK', [('Content-type', 'text/html')])
    filePage = open('templates/filePage.html','r').read()
    filePage = filePage.replace("#PATH#",env['PATH_INFO']) 
    return [filePage]

def dirPage(env,resp):
    resp('200 OK', [('Content-type', 'text/html')])
    dirPage = open('templates/dirPage.html','r').read()
    dirPage = dirPage.replace("#PATH#",env['PATH_INFO']) 
    return [dirPage]

urls = [(r'^$',login),
        (r'filesStructure/?$',fileStructure),
        (r'filePage/?(.*)',filePage),
        (r'dirPage/?(.*)',dirPage),]

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def app(env, resp):
    path = env.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            env['myapp.url_args'] = match.groups()
            return callback(env, resp)
    return not_found(env, resp)

   

server=simple_server.make_server('', 8000, app)
server.serve_forever()