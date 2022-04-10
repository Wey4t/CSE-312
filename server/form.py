from request import *
class Form:
    def __init__(self, request, names):
        self.table = {}
        pass





if __name__ == "__main__":
    test_case_1 = b'POST /sign-in HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 256\r\nCache-Control: max-age=0\r\nsec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/SignIn.html\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7\r\n\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nContent-Disposition: form-data; name="user_name"\r\n\r\nTom Aan\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nContent-Disposition: form-data; name="user_password"\r\n\r\nZSZDaawu!\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap--\r\n'
    names_1 = ['user_name','user_password']
    request_1 = Request(test_case_1,'')
    form_1 = Form(request_1,names_1)
    if form_1.table['user_name'] == 'Tom Aan':
        print('true')
    if form_1.table['user_password'] == 'ZSZDaawu!':
        print('true')
