
import socketserver
from request import Request
from router import Router
from dm import add_dm_path
from static_file_path import add_file_path
from user_info import add_user_path
from user_profile import add_profile_path
from user_chat import add_chat_path
from settings import add_settings_paths
import websocket
import sys
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    ws_users = {} # store username:handler object to identity the ws connections

    router = Router()
    add_settings_paths(router)
    add_dm_path(router)
    add_chat_path(router)
    add_user_path(router)
    add_profile_path(router)
    websocket.add_websocket_path(router)
    add_file_path(router)
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4*1024).strip()
        if len(self.data) == 0:
            return 
        print("{} wrote:".format(self.client_address[0]))
        
        request = Request(self.data, self)
        self.router.handle_request(request, self)
        sys.stdout.flush()
        sys.stderr.flush()
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080

    # Create the server, binding to localhost on port 8080
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
