import json
import bcrypt
import secrets
import hashlib
from router import add_route, Route
from database import *
from response import generate_response, redirect
from form import Form
TOKEN_LEN = 80
AUTH_COOKIE = 'auth_tk'  # the name of authorized token

def add_user_path(router):
    router.add_route(Route('POST', '/login', login_user))
    router.add_route(Route('POST', '/register', register_user))
    router.add_route(Route('POST', '/logout', logout))
    router.add_route(Route('POST','/profile_post',profile))
    router.add_route(Route('POST','/content_post',content))
def content(request,handler):
    names= ['content']
    form_data = Form(request,names).table
    for key in form_data:
        form_data[key] =  form_data[key].decode()
    token = request.cookies[AUTH_COOKIE]
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    user_info = find(USER, {'token':hash_token})
    auth_name = user_info['username']
    update(PROFILE,{'username':auth_name},{'post':form_data['content']})

    handler.request.sendall(redirect('/'))
def profile(request,handler):
    names= ['profile']
    form_data = Form(request,names).table
    for key in form_data:
        form_data[key] =  form_data[key].decode()
    token = request.cookies[AUTH_COOKIE]
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    user_info = find(USER, {'token':hash_token})
    auth_name = user_info['username']
    update(PROFILE,{'username':auth_name},form_data)

    handler.request.sendall(redirect('/'))

def logout(request,handler):
    if check_user(request):
        token = request.cookies[AUTH_COOKIE]
        hash_token = hashlib.sha256(token.encode()).hexdigest()
        user_info = find(USER, {'token':hash_token})
        username = user_info['username']
        query = find(USER_STATUS, {'username':username})
        if query is None:
            handler.request.sendall(generate_response(b'Not such user','text/plain','404 Not Found'))
        else:
            if( query['status'] == 'online'):
                update(USER_STATUS, {'username':username},{'status': 'offline'})
    else:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))

def register_user(request, handler):
    parsed_form = Form(request, ["username", "password"])
    username = parsed_form.table["username"]
    password = parsed_form.table["password"]
    if registration(username.decode(), password):
        handler.request.sendall(redirect('/src/SignIn.html'))

def registration(username, password):
    if username is bytes:
        username = username.decode()
    if type(password) is not bytes:
        password = password.encode()
    salt = bcrypt.gensalt()  # salt and hash are string in database
    hashed = bcrypt.hashpw(password, salt).decode()
    new_user = {
        'username': username,
        'hash': hashed,
        'token': 'never log in',
        'salt': salt.decode()
    }
    new_user_profile = {
        'username': username,
        'post': 'This user is lazzy, post nothing',
        'profile':'This user have not any description',
        'profile_image':'default.png'
    }
    insert(new_user)
    insert(new_user_profile)
    return True

def login_user(request, handler):
    parsed_form = Form(request, ["username", "password"])
    username = parsed_form.table["username"].decode()
    password = parsed_form.table["password"]
    query = find(USER, {'username':username})
    if query == None:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))
    hashed = query['hash']
    if type(password) is not bytes:
        password = password.encode()
    if type(hashed) is not bytes:
        hashed = hashed.encode()
    if bcrypt.checkpw(password,hashed):
        [token, hash_tokne] = generate_auth_token()
        update(USER, {'username':username},{'token':hash_tokne})
        query = find(USER, {'username':username})
        headers = []
        headers.append(b'Set-Cookie: %s='%AUTH_COOKIE.encode() + token.encode() + b'; HttpOnly; Max-Age=3600')
        query = find(USER_STATUS, {'username':username})
        if query is None:
            insert({'username':username,'status':'online'})
        else:
            if( query['status'] == 'online'):
                update(USER_STATUS, {'username':username},{'status': 'online'})
        handler.request.sendall(generate_response(b'You login',headers=headers))
    else:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))

def check_user(request):
    token = request.cookies.get(AUTH_COOKIE)
    if  token == None:
        return False
    if '------' in token:
        token = token.split('------')[0]
    print(token)
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    user = find(USER, {'token':hash_token})
    if user == None: #no such user
        return False
    else:
        return True

def generate_auth_token():
    token = secrets.token_urlsafe(TOKEN_LEN)
    hash_token = hashlib.sha256(token.encode()).hexdigest()
    return [token, hash_token]

