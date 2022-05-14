import json
import bcrypt
import secrets
import hashlib
from request import *
from form import *
from router import add_route, Route
from database import *
from response import generate_response, redirect
from websocket import constructResponseFrame
def add_dm_path(router):
    router.add_route(Route('POST','^/DM',add_dm))

def add_dm(request, handler):
    names= ['sender','receiver','message']
    form_data = Form(request,names).table
    for key in form_data:
        form_data[key] =  form_data[key].decode()
    form_data.update({"message_status":"unread"})
    #print(form_data)
    insert(form_data)
    receiver = form_data['receiver']
    for connection in handler.ws_users:
        name,nop = connection.split('/')
        if name == form_data['receiver']:
            try:
                dict = {'type':'pong'}
                handler.ws_users[connection].request.sendall(constructResponseFrame(dict))
                dict = {'type':'chat_pong', 'sender': form_data['sender']}
                handler.ws_users[connection].request.sendall(constructResponseFrame(dict))
            except:
                del handler.ws_users[connection]
    handler.request.sendall(redirect('chat/'+receiver))


