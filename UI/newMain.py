from wsgiref.util import setup_testing_defaults
from wsgiref import simple_server
import cgi
import UIGenerator
import json

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def app(env, resp):
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
        with open('templates/test.json') as data_file: 
			jsonFile = json.load(data_file)
        login = UIGenerator.generateFileTreePage(jsonFile)
    return [login]

server=simple_server.make_server('', 8000, app)
server.serve_forever()