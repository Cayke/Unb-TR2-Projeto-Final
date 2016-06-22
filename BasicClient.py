import socket
import json
import Define

IP = '127.0.0.1'  # Server IP
PORTSERVER = 3301  # Server PORT
__PORTCLIENT = 4578  # Client PORT to recive DHT files


# Register a user
# param: username - The username to register in database
# return: SUCCESS/ERROR CODE
def register(username):
    msg = '{"username" : "' + username + '", "type" : ' + Define.CADASTRO + ' }'
    jsonmsg = json.loads(msg)

    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        return Define.FAILEDCREATESOCK

    dest = (IP, PORTSERVER)
    tcp.connect(dest)

    try:
        tcp.send(jsonmsg)
    except socket.error:
        # Send failed
        print 'Send failed'
        return Define.SENDFAILED

    response = tcp.recive(126)
    if response["responseStatus"] == Define.SUCCESS:
        return response["id"]
    else:
        return response["ERROR CODE"]


# Login a user
# param: username - The username to login
# return: SUCCESS/ERROR CODE
def login(username):
    msg = '{"username" : "' + username + '", "type" : ' + Define.LOGIN + ' }'
    jsonmsg = json.loads(msg)

    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        return Define.FAILEDCREATESOCK

    dest = (IP, PORTSERVER)
    tcp.connect(dest)

    try:
        tcp.send(jsonmsg)
    except socket.error:
        # Send failed
        print 'Send failed'
        return Define.SENDFAILED

    response = tcp.recive(126)
    if response["responseStatus"] == Define.SUCCESS:
        return response["id"]
    else:
        return response["ERROR CODE"]


# Upload file to server
# param: path - The path of the file
# param: filename - Name of the file
# return: SUCCESS/ERROR CODE
def upload(path, filename):
    pass


# Download file from server
# param: path - The path of the file including file name
# return: SUCCESS/ERROR CODE (if success file will be writen in a folder)
def download(path):
    pass


def __downloadhash(hash):
    pass
