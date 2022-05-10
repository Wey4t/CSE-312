import hashlib
import os
import time
from typing import Dict
from router import add_route, Route
from user_info import check_user, AUTH_COOKIE
from response import generate_response
from template_engine import *
from database import *
CHAT_TEMPLATE_PATH = 'src/template/chat_template.html'
CHAT_TEMPLATE_DEFAULT_PATH = 'src/template/chat_template_default.html'
def add_chat_path(router):
    router.add_route(Route('GET','chat/[0-9a-zA-Z]*',chat))

def chat(request, handler):
    print(name)
    if check_user(request):
       data:dict = construct_template_data(request)
       #print(os.getcwd())
       view = make_template(CHAT_TEMPLATE_PATH,data)
       handler.request.sendall(generate_response(view.encode('utf-8'),'text/html; charset=utf-8'))
    else:
       handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))

def construct_template_data(request):
    name = request.path[request.path.rfind('/')+1 : ]
    token = request.cookies[AUTH_COOKIE]
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    user_info = find(USER, {'token':hash_token})
    auth_name = user_info['username']
    messages1 = find_all(MESSAGE, {'sender':auth_name,'receiver':name})
    messages2 = find_all(MESSAGE, {'sender':name,'receiver':auth_name})
    messages = messages1 + messages2
    loop_data_messages = []
    for message in messages:
        data = {
                   'hidden_chat_user' : 'fill',
                   'chat_user' : 'fill',
                   'time' : 'fill',
                   'message' : 'fill',
                   'hidden_auth_user' : 'fill',
                   'time' : 'fill',
                   'auth_message' : 'fill'
               }
        loop_data_messages.append(data)
    loop_dict = {
        'start_tag' : '{{loop_user_chat_history_start}}',
        'end_tag' : '{{loop_user_chat_history_end}}',
    }
    loop_dict['data'] = gloop_data_messages
    dict = {
            'auth_user_image' : 'fill',
            'chat_user_image' : 'fill',
            'user' : 'fill',
            'data' : loop_data_messages
        }
    return dict