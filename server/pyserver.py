import socketserver
from request import Request
from router import Router
from static_file_path import add_file_path
import websocket
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    ws_users = {} # store username:handler object to identity the ws connections

    router = Router()
    websocket.add_websocket_path(router)
    add_file_path(router)
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if len(self.data) == 0:
            return 
        print("{} wrote:".format(self.client_address[0]))
        
        request = Request(self.data, self)
        self.router.handle_request(request, self)
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    # Create the server, binding to localhost on port 8080
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
