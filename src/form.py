from request import *
class Form:
    def __init__(self, request, names):
        self.table={}
        if first_form_name(request.body) in names:
            self.table[first_form_name(request.body)] = firstValue(request.body)
        if second_form_name(request.body) in names:
            self.table[second_form_name(request.body)] = secondValue(request.body)
        else:
            return 

def first_form_name(data:bytes):
    form_name = data.split(Request.blank_line)[0]
    form_name = form_name[form_name.find(b'name='):].split(b'"')[1]
    return form_name.decode()

def second_form_name(data: bytes):
    form_name = data.split(Request.blank_line)[1]
    form_name = form_name[form_name.find(b'name='):].split(b'"')[1]
    return form_name.decode()

def firstValue(data: bytes):
    username=data.split(Request.blank_line)[1].split(Request.new_line)[0]
    return username.decode()

def secondValue(data: bytes):
    password = data.split(Request.blank_line)[2].split(Request.new_line)[0]
    return password.decode()

if __name__ == "__main__":
    test_case_1 = b'POST /sign-in HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 256\r\nCache-Control: max-age=0\r\nsec-ch-ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/SignIn.html\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7\r\n\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nContent-Disposition: form-data; name="user_name"\r\n\r\nTom Aan\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap\r\nContent-Disposition: form-data; name="user_password"\r\n\r\nZSZDaawu!\r\n------WebKitFormBoundaryZ1WXYkJKPvmf4Bap--\r\n'
    test_case_2 = b'POST /image-upload HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 291\r\nCache-Control: max-age=0\r\nsec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundary4SFDXMP54QDHBbyE\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: Idea-92bea270=2f742a5d-6ddf-417e-94d0-8ead8e74af13\r\n\r\n------WebKitFormBoundary4SFDXMP54QDHBbyE\r\nContent-Disposition: form-data; name="comment"\r\n\r\n1231312\r\n------WebKitFormBoundary4SFDXMP54QDHBbyE\r\nContent-Disposition: form-data; name="upload"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundary4SFDXMP54QDHBbyE--\r\n'
    names_1 = ['user_name','user_password']
    name_2 = ['comment','123']
    request_1 = Request(test_case_1,'')
    request_2 = Request(test_case_2,'')
    form_1 = Form(request_1,names_1)
    form_2 = Form(request_2,name_2)
    print (form_1.table)
    print(form_2.table)