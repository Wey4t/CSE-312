import imp
from router import add_route, Route
from response import generate_response,redirect
from user_info import check_user
import os

def sent_file(request, handler):
    filepath = request.path.strip('/')    # strip root '/'
    filename = filepath[filepath.rfind('/')+1 : ]  # get path/to/file file name
    filetype = filename[filename.rfind('.')+1 : ]  # file.type  get  type
    if os.path.exists(filepath):
        if filetype == 'jpeg' or filetype == 'jpg' or filetype == 'png':
            handler.request.sendall(try_open_file(filepath,handler,'image/%s'%filename))
        elif filetype == 'css':
            handler.request.sendall(try_open_file(filepath,handler,'text/css; charset=utf-8'))
        elif filetype == 'html':
            handler.request.sendall(try_open_file(filepath,handler,'text/html'))
        elif filetype == 'js':
            handler.request.sendall(try_open_file(filepath,handler,'text/javascript; charset=utf-8'))
    else:
        handler.request.sendall(generate_response(b'content was not found','text/plain','404 Not Found'))
def home(request, handler):
    if check_user(request):
        handler.request.sendall(redirect('/profile'))
    else:
        handler.request.sendall(redirect('/src/SignIn.html'))

def try_open_file(filename, handler, type, flag='rb'):
    fp = open(filename,flag)
    return generate_response(fp.read(), type)

def add_file_path(router):
    router.add_route(Route('GET','^/.*\.html$',sent_file))
    router.add_route(Route('GET','^/.*\.css$',sent_file))
    router.add_route(Route('GET','^/.*\.js$',sent_file))
    router.add_route(Route('GET','^/.*\.png$',sent_file))
    router.add_route(Route('GET','^/.*\.jpg$',sent_file))
    router.add_route(Route('GET','^/$',home))