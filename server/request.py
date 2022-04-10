class Request:
    new_line = b'\r\n'
    blank_line = b'\r\n\r\n'
    def __init__(self, http_request, handler):
        if(b'Content-Type: multipart/form-data' in http_request):
            http_request = buffer_form(http_request, handler)
        self.received_length = len(http_request)
        [request_line, self.header, self.body] = parse_request(http_request)
        [self.method, self.path, self.version] = request_line.decode().split(' ')

###################################
#  buffer the remain request body.
# 
# ##############       
def buffer_form(http_request, handler):
    length = get_form_length(http_request)
    cur_length = get_current_length(http_request)
    while cur_length < length:
        data = handler.request.recv(1024)
        cur_length += len(data)
        print('receiving:',cur_length, '/', length)        
        http_request += data
    return http_request
def parse_request(data: bytes): #assume have data
    request_line = data[0: data.find(Request.new_line)] # http class
    header = data[data.find(Request.new_line)+len(Request.new_line): data.find(Request.blank_line)+len(Request.blank_line)] # http class
    index_before_content = data.find(Request.blank_line)+len(Request.blank_line)
    if data.find(Request.blank_line) == -1:
        body = b''
    else:
        body = data[index_before_content : ]
    return [request_line,header,body]
def get_length(header: bytes):
    index = header.find(b'Content-Length:')+len(b'Content-Length:')
    body = header[index : ]
def get_form_length(header:bytes):
    index = header.find(b'Content-Length:')+len(b'Content-Length:')
    body = header[index : ]
    return int(body[:body.find(Request.new_line)])
def get_current_length(header:bytes):
    index = header.find(Request.blank_line)
    if index == -1:
        return len(Request.blank_line)
    return (len(header) - index -len(Request.blank_line))


if __name__ == "__main__":
    test_case_1 = b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: cross-site\r\nSec-Fetch-Mode: navigate\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7,eo;q=0.6'
    r = Request(test_case_1,'')
    print('method:',r.method)
    print('version:',r.version)
    print('length:',r.received_length)
    print('body:',r.body)

