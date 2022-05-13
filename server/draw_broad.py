from router import Route
from template_engine import *
from response import generate_response
from database import *
from settings import get_username

def add_drawboard_path(router):
    router.add_route(Route('GET', '/drawboard', render_drawboard))

def render_drawboard(request, handler):
    username = get_username(request)
    if username == "":
        handler.request.sendall(generate_response(b'Your submission was rejected','text/plain','403 Forbidden'))
        return
    user_pfp = find(PROFILE, {"username":username})["profile_image"]
    drawboard_page = make_template("./src/template/draw_borad_template.html", {"auth_user_image":user_pfp})
    handler.request.sendall(generate_response(drawboard_page.encode(), 'text/html; charset=utf-8'))