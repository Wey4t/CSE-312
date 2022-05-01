import re
from response import generate_response
def add_route(route):
    Router.routes.append(route)
class Router:
    routes = []
    def add_route(self,route):
        Router.routes.append(route)
    def handle_request(self, request, handler):
        for route in self.routes:
            if route.is_request_match(request):
                route.handle_request(request, handler)
                return
        handler.request.sendall(generate_response(b'content was not found','text/plain','404 Not Found'))
        # return 404



class Route:
    def __init__(self, method, path, action):
        self.method = method
        self.path = path
        self.action = action
    def is_request_match(self, request):
        return request.method == self.method and re.search(self.path,request.path)
    def handle_request(self,request, handler):
        self.action(request,handler)
    
