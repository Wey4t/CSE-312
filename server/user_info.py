<<<<<<< HEAD
import json
import bcrypt
import secrets
import hashlib
from router import add_route, Route
from database import *
from response import generate_response
from form import Form
TOKEN_LEN = 80
AUTH_COOKIE = 'auth_tk'  # the name of authorized token

def add_user_path(router):
    router.add_route(Route('POST', '/login', login_user))
    router.add_route(Route('POST', '/register', register_user))

def register_user(request, handler):
    parsed_form = Form(request, ["username", "password"])
    username = parsed_form.table["username"]
    password = parsed_form.table["password"]
    registration(username, password)

def registration(username, password):
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
        'profile':'This user have not any profile',
        'profile_image':'default.png'
    }
    insert(new_user)
    insert(new_user_profile)

def login_user(request, handler):
    parsed_form = Form(request, ["username", "password"])
    username = parsed_form.table["username"]
    password = parsed_form.table["password"]
    query = find(USER, {'username':username})
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
        handler.request.sendall(generate_response(b'You login',headers=headers))
    else:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))

def check_user(request):
    if request.cookies.get(AUTH_COOKIE) == None:
        return False
    print(request.cookies[AUTH_COOKIE])
    token = request.cookies[AUTH_COOKIE]
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

=======
import json
import bcrypt
import secrets
import hashlib
from router import add_route, Route
from database import *
from response import generate_response
TOKEN_LEN = 80
AUTH_COOKIE = 'auth_tk'  # the name of authorized token
def add_user_path(router):
    router.add_route(Route('POST','^/users',add_user))
    router.add_route(Route('GET','^/users/[0-9a-z-A-Z]',login))
    router.add_route(Route('GET','^/name',check_test))
def add_user(request, handler):
    josnstring = request.body.decode()
    user_dict = json.loads(josnstring) 
    registration(user_dict)

def registration(dic):
    password = dic['password']
    if type(password) is not bytes:
        password = password.encode()
    salt = bcrypt.gensalt()  # salt and hash are string in database
    hashed = bcrypt.hashpw(password, salt).decode()
    new_user = {
        'username': dic['username'],
        'email': dic['email'],
        'hash': hashed,
        'token': 'never log in',
        'salt': salt.decode()
    }
    new_user_profile = {
        'username': dic['username'],
        'post': 'This user is lazzy, post nothing',
        'profile':'This user have not any profile',
        'profile_image':'default.png'
    }
    insert(new_user)
    insert(new_user_profile)

def login(request, handler):
    josnstring = request.body.decode()
    user_dict = json.loads(josnstring) 
    password = user_dict['password']
    username = user_dict['username']
    query = find(USER, {'username':username})
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
        handler.request.sendall(generate_response(b'You login',headers=headers))
    else:
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))
def check_user(request):
    if request.cookies.get(AUTH_COOKIE) == None:
        return False
    print(request.cookies[AUTH_COOKIE])
    token = request.cookies[AUTH_COOKIE]
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

def check_test(request,handler):
    print(check_user(request))
>>>>>>> 23ac1d15266811e6cb470e99bf7269eefacc9cd7
