from form import Form
from database import *
from user_info import *
from response import *
from router import add_route, Route
import sys

def add_settings_paths(router):
    router.add_route(Route('POST', "/upload-pfp", upload_user_pfp))

def upload_user_pfp(request, handler):
    parsed_form = Form(request, ["icon","dd"])
    image_bytes = parsed_form.table["icon"]
    print("image: ", image_bytes)
    last_pfp_id = find(PFP_ID)
    pfp_id = 0
    username = get_username(request)

    if username == "":
        return

    if last_pfp_id:
        pfp_id = last_pfp_id["last_pfp_id"] + 1
        update(PFP_ID, {}, {"last_pfp_id": pfp_id}, False)
    else:
        insert({"last_pfp_id": 0})

    img_filename = "user_image" + str(pfp_id) + ".jpg"

    if image_bytes != b'':
        with open("./src/staticFile/image/"+img_filename, "wb") as user_img:
            user_img.write(image_bytes)
    
    update(PROFILE, {"username":username}, {"profile_image":img_filename}, False)
    handler.request.sendall(redirect("/profile"))
    sys.stdout.flush()
    sys.stderr.flush()


def get_username(request):
    if check_user(request):
        token = request.cookies.get(AUTH_COOKIE)
        if  token == None:
            return False
        if '------' in token:
            token = token.split('------')[0]
        print(token)
        print('token',token)
        hash_token = hashlib.sha256(token.encode()).hexdigest()
        user_info = find(USER, {'token':hash_token})
        username = user_info['username']
        return username
    return ""


