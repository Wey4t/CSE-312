from form import Form
from database import *
from user_info import *
from response import *

def upload_user_pfp(request, handler):
    parsed_form = Form(request, ["pfp_upload"])
    image_bytes = parsed_form.table["pfp_upload"]
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

    img_filename = "user_image" + pfp_id + ".jpg"

    if image_bytes != b'':
        with open("../src/staticFile/image/"+img_filename, "wb") as user_img:
            user_img.write(image_bytes)
    
    update(PROFILE, {"username":username}, {"profile_image":img_filename}, False)
    handler.request.sendall(redirect("src/profile.html"))


def get_username(request):
    if check_user(request):
        token = request.cookies[AUTH_COOKIE]
        hash_token = hashlib.sha256(token.encode()).hexdigest()
        user_info = find(USER, {'token':hash_token})
        username = user_info['username']
        return username
    return ""
    


