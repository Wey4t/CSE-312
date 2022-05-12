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
    router.add_route(Route('GET','^/chat/[0-9a-zA-Z]{1,25}',chat))
    router.add_route(Route('GET','^/chat_default',chat_default))

def chat_default(request,handler):
    if not check_user(request):
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))
        return
    data = {}
    loop_dict = construct_online_user(request,data)
    data['loop_data'] = []
    data['loop_data'].append(loop_dict)
    print(data)
    print(handler.ws_users)
    view = make_template(CHAT_TEMPLATE_DEFAULT_PATH,data)
    handler.request.sendall(generate_response(view.encode('utf-8'),'text/html; charset=utf-8'))

def construct_online_user(request,data):
    token = request.cookies[AUTH_COOKIE]
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    user_info = find(USER, {'token':hash_token})
    user_profile = find(PROFILE, {'username':user_info['username']})
    auth_name = user_info['username']
    #online_user = handler.ws_users
    online_users = find_all(USER_STATUS, {'status':'online'})
    users = []
    sender_dict = {}
    loop_online_user = []
    unread_messages = find_all(MESSAGE, {'receiver':auth_name,'message_status':'unread'})
    print('unreads',unread_messages)
    if unread_messages is not None:
        for unread_message in unread_messages:
            sender_dict[unread_message['sender']] = '1'
    for user in online_users:
        if(user['username'] != auth_name):
            users.append(user['username'])
    if data.get('auth_user_image') == None:
        data['auth_user_image']=user_profile['profile_image']
    print('test',sender_dict)
    for key in users:
        if key is bytes:
            key = key.decode()
        user_query = find(PROFILE, {'username':key})
        hidden_noti = 'hidden'
        if(sender_dict.get(key) is not None and sender_dict[key] == '1'):
            hidden_noti = ''
            print(key,hidden_noti)
        user_data = {
                   'online_user_image': user_query['profile_image'],
                   'noti_online_user' : hidden_noti,
                   'online_users': key,
                   'id' : key
               }
        loop_online_user.append(user_data)
    print('ad',user_data)
    loop_dict = {
        'start_tag' : '{{loop_online_user_start}}',
        'end_tag' : '{{loop_online_user_end}}',
    }
    loop_dict['datas'] = loop_online_user
    return loop_dict
def chat(request, handler):
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
    user_image = find(PROFILE,{'username':auth_name})
    chat_user_image = find(PROFILE,{'username': name})
    chat_image = chat_user_image['profile_image']
    auth_image = user_image['profile_image']
    messages1 = find_all(MESSAGE, {'sender':auth_name,'receiver':name})
    messages2 = find_all(MESSAGE, {'sender':name,'receiver':auth_name})
    messages = []
    i=0
    j=0
    N=len(messages1)
    M= len(messages2)
    while i<N and j<M:
        if str(messages1[i]['_id'])< str(messages2[j]['_id']) :
            messages.append(messages1[i])
            i+=1
        else:
            messages.append(messages2[j])
            j+=1
    while i <N :
        messages.append(messages1[i])
        i+=1
    while j<M:
        messages.append(messages2[j])
        j+=1
    loop_data_messages = []
    hidden = 'hidden'
    auth_hidden = ''
    auth_message =''
    loop_data =[]
    for message in messages:
        print(message['receiver'])
        if auth_name != message['sender']:
            hidden = ''
            auth_hidden = 'hidden'
        else:
            hidden='hidden'
            auth_hidden =''
        data = {
                   'hidden_chat_user' : hidden,
                   'chat_user' : name,
                   'time' : '',
                   'message' : message['message'],
                   'hidden_auth_user' : auth_hidden,
                   'time' : '',
                   'auth_message' : message['message'],
               }
        loop_data_messages.append(data)
    loop_dict = {
        'start_tag' : '{{loop_user_chat_history_start}}',
        'end_tag' : '{{loop_user_chat_history_end}}',
    }
    loop_dict['datas'] = loop_data_messages
    dict = {
            'auth_user_image' : auth_image,
            'chat_user_image' : chat_image,
            'auth_user':auth_name,
            'chat_user':name,
            'user' : name,
            'loop_data' : loop_data
        }
    dict['loop_data'].append(loop_dict)
    dict['loop_data'].append(construct_online_user(request,dict))
    print(dict)
    return dict

if __name__ =="__main__":
    user1 = 'flower'
    auth_user = 'sun'
    messages1 = find_all(MESSAGE, {'sender':auth_user,'receiver':user1})
    messages2 = find_all(MESSAGE, {'sender':user1,'receiver':auth_user})
    message1 = messages1 + messages2
    message2 = []
    i=0
    j=0
    N=len(messages1)
    M= len(messages2)
    while i<N and j<M:
        if str(messages1[i]['_id'])< str(messages2[j]['_id']) :
            message2.append(messages1[i])
            i+=1
        else:
            message2.append(messages2[j])
            j+=1
    while i <N :
        message2.append(messages1[i])
        i+=1
    while j<M:
        message2.append(messages2[j])
        j+=1
    print("1",message1)
    print("2",message2)
	