import re
class Router:
    def __init__(self):
        self.routes = []
    def add_route(self,route):
        self.routes.append(route)
    def handle_request(self, request, handler):
        for route in self.routes:
            if route.is_request_match(request):
                route.handle_request(request, handler)
                return
        # return 404



class Route:
    def __init__(self, method, path, action):
        self.method = method
        self.path = path
        self.action = action
    def is_request_match(self, request):
        return request.method == self.method and re.search('^'+self.path,request.path)
    def handle_request(self,request, handler):
        self.action(request,handler)

if __name__ == "__main__":
    class Request:
        def __init__(self,method,path):
            self.method = method
            self.path = path
    def test_func(request,handler):
        print('t21312est')
    Router.add_route(Route('GET','/hello',test_func))

    r = Router()
    request = Request('GET','/hello')
    r.handle_request(request,'')
