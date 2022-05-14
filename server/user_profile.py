import hashlib
import os
import time
from typing import Dict
from router import add_route, Route
from user_info import check_user, AUTH_COOKIE
from response import generate_response
from template_engine import *
from database import *
PROFILE_TEMPLATE_PATH = 'src/template/profile_template.html'
def add_profile_path(router):
    router.add_route(Route('GET','profile',profile))


def profile(request, handler):
    if check_user(request):
        data:dict = construct_template_data(request)
        ##print(os.getcwd())
        view = make_template(PROFILE_TEMPLATE_PATH,data)
        handler.request.sendall(generate_response(view.encode('utf-8'),'text/html; charset=utf-8'))
    else:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))

def construct_template_data(request):
    token = request.cookies[AUTH_COOKIE]
    #print(token)
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    #print('hashtoken:',hash_token)
    user_info = find(USER, {'token':hash_token})
    user_profile = find(PROFILE, {'username':user_info['username']})
    dict = {
        'username': user_info['username'],
        'Personal_profile': user_profile['profile'],
        'content': user_profile['post'],
        'auth_user_image': user_profile['profile_image'],
        'time': time.strftime("%H:%M:%S", time.localtime()),
        'status': 'online',
        'noti': 'hidden'
    }
    return dict

if __name__ == "__main__":
    #print(os.getcwd())
    fp = open('src/template/profile_template.html','rb')
    #print(fp.read())