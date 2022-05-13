def generate_response(body:bytes, content_type:str = 'text/plain; charset=utf-8', status_code = '200 OK', headers = []):
    response = ('HTTP/1.1 %s\r\nContent-Length: %s\r\nContent-type: %s\r\nX-Content-Type-Options: nosniff'\
    %(status_code,str(len(body)),content_type)).encode()
    for header in headers:
        response += b'\r\n' + header
    response += b'\r\n\r\n'
    response += body
    return response

def redirect(path):
    response = ('HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: %s\r\n\r\n' % path).encode()
    return response

def redirect_via_cookies(path, cookies):
    data = b''
    for i in cookies:
        data += i
    response = ('HTTP/1.1 302 Redirect\r\nContent-Length: 0\r\nLocation: %s\r\n' % path).encode() + data + b'\r\n\r\n'
    return response

