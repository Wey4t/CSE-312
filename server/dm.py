import json
import bcrypt
import secrets
import hashlib
from request import *
from form import *
from router import add_route, Route
from database import *
from response import generate_response, redirect

def add_dm_path(router):
    router.add_route(Route('POST','^/DM',add_dm))

def add_dm(request, handler):
    names= ['sender','receiver','message']
    form_data = Form(request,names).table
    for key in form_data:
        form_data[key] =  form_data[key].decode()
    print(Form(request,names).table)
    print(form_data)
    insert(form_data)
    handler.request.sendall(redirect('/src/template/chat_template.html'))


