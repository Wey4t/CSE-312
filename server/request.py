class Request:
    new_line = b'\r\n'
    blank_line = b'\r\n\r\n'
    def __init__(self, http_request, handler):
        if(b'Content-Type: multipart/form-data' in http_request):
            [http_request,self.boundary] = buffer_form(http_request, handler)
        self.received_length = len(http_request)
        [request_line, self.headers, self.body] = parse_request(http_request)
        [self.method, self.path, self.version] = request_line.decode().split(' ')
        self.cookies = pareseCookie(self.headers)
###################################
#  buffer the remain request body.
# 
# ##############       
def buffer_form(http_request, handler):
    http_request += Request.blank_line
    length = get_form_length(http_request)
    cur_length = get_current_length(http_request)
    while cur_length < length:
        data = handler.request.recv(8*1024)
        cur_length += len(data)
        #print('receiving:',cur_length, '/', length)        
        http_request += data
    endboundary = http_request[http_request.strip(Request.new_line).rfind(Request.new_line)+len(Request.new_line): ].strip(Request.new_line)
    boundary = endboundary[ : -2]
    return [http_request, boundary]
def parse_request(data: bytes): #assume have data
    request_line = data[0: data.find(Request.new_line)] # http class
    if data.find(Request.blank_line) == -1:
        body = b''
        header = data[data.find(Request.new_line)+len(Request.new_line): ] # http class
    else:
        index_before_content = data.find(Request.blank_line)+len(Request.blank_line)
        body = data[index_before_content : ]
        header = data[data.find(Request.new_line)+len(Request.new_line): data.find(Request.blank_line)+len(Request.blank_line)].strip(Request.new_line)
    headers = parseHeaders(header.decode())
    return [request_line,headers,body]
def get_form_length(header:bytes):
    index = header.find(b'Content-Length:')+len(b'Content-Length:')
    body = header[index : ]
    return int(body[:body.find(Request.new_line)])
def get_current_length(header:bytes):
    index = header.find(Request.blank_line)
    if index == -1:
        return 0
    return (len(header) - index)
# parse the headers string and output a dictionary
def parseHeaders(headers: str):
    headers = headers.split("\r\n")
    retVal = {}
    for header in headers:
        pair = header.split(":")
        # remove the empty spaces in the key/value if any
        retVal[pair[0].replace(" ", "")] = pair[1].replace(" ", "")
    return retVal
def pareseCookie(headers):
    ans = {}
    if headers.get('Cookie') is not None:
        cookies = headers['Cookie']
        cookies = cookies.split(';')
        for cookie in cookies:
            cookie_pair = cookie.split('=')
            ans[cookie_pair[0].strip()] = cookie_pair[1].strip()
    return ans

