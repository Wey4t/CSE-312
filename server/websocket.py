from router import Route
from response import generate_response
import database as db
import json
import hashlib
import base64
import sys
#from pyserver import MyTCPHandler as myTCPHandler
import random

def add_websocket_path(router):
    router.add_route(Route("GET", "/websocket", connectWS))
    #router.add_route(Route("GET", "/chat-history", getChatHistory))


def connectWS(request, handler):

    # handshake with the client, computes the sha1Hash and encode it with base64 as the accept key
    headers = request.headers
    wsKey = headers["Sec-WebSocket-Key"]
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1Hash = base64.b64encode(hashlib.sha1((wsKey + GUID).encode()).digest())
    response = "HTTP/1.1 101 Switching Protocols\r\n"
    response += "Content-Length: 0\r\n"
    response += "Connection: Upgrade\r\n"
    response += "Upgrade: websocket\r\n"
    response += "Sec-WebSocket-Accept: " 
    response = response.encode() + sha1Hash + ("\r\n\r\n").encode()
    handler.request.sendall(response)

    # listen for the websocket data until the client sever the connection
    # for this hw, we assume FIN bit is always 1, RSVs are always 0,
    # opcode is either 0001(sending txt) or 1000(close connection), so first byte is either 129/136
    username = "User" + str(random.randint(0, 1000))
    handler.ws_users[username] = handler

    while True:

        #print("-----------------------------------")

        ws_data = handler.request.recv(2)
        print(ws_data)
        print("Start receiving new message...")

        if ws_data[0] == 136:
            # close connection, remove the user from the ws_users
            print("Connection Closed")
            del handler.ws_users[username]
            return

        if ws_data[0] != 129:
            continue

        print("Prebits: ", ws_data[0])
        
        payload_len = ws_data[1] & 0b01111111
        extended_len = 0
        print("Payload_len: " + str(payload_len))
        masking_keys_idx = 0

        # buffer ws_data as needed
        total_len = 0
        if payload_len == 127:
            extended_len_bytes = handler.request.recv(8)
            ws_data += extended_len_bytes
            extended_len = int.from_bytes(extended_len_bytes, "big")
            masking_keys_idx = 10
            total_len = 14 + extended_len
        elif payload_len == 126:
            extended_len_bytes = handler.request.recv(2)
            ws_data += extended_len_bytes
            extended_len = int.from_bytes(extended_len_bytes, "big")
            masking_keys_idx = 4
            total_len = 8 + extended_len
        else:
            masking_keys_idx = 2
            total_len = 6 + payload_len
        while len(ws_data) < total_len:
            data = handler.request.recv(total_len - len(ws_data))
            ws_data += data
            print("Receiving: ", len(ws_data), " / ", total_len)


        payload_start_idx = masking_keys_idx + 4
        print("Extended_len: " + str(extended_len))
        processed_data = []
        print("Total data len is: ", len(ws_data))
        # XORed the payload with the masking_keys
        for i in range(payload_start_idx, len(ws_data)):
            if masking_keys_idx == payload_start_idx:
                masking_keys_idx -= 4
            processed_data.append(ws_data[i] ^ ws_data[masking_keys_idx])
            masking_keys_idx += 1
        
        processed_data = bytearray(processed_data)
        dataDict = json.loads(processed_data)

        # check the messagetype, forward to another user if type is not "chatMessage"
        if dataDict["messageType"] != "chatMessage":
            for user_handler in handler.ws_users.values():
                if user_handler != handler:
                    response_frame = constructResponseFrameFromBytes(processed_data)
                    user_handler.request.sendall(response_frame)
                    print(dataDict)
                    print(handler, " to ", user_handler)
                    print("")
            continue


        dataDict["comment"] = escape_html(dataDict["comment"])
        print("Comment len is: ", len(dataDict["comment"]))
        dataDict["username"] = username
        #print(dataDict)

        response_frame = constructResponseFrame(dataDict)

        # insert the chat into the chat history database
        del dataDict["messageType"]
        # db.storeChat(dataDict)

        # broadcast the response frame to all the connected users
        for user_handler in handler.ws_users.values():
            user_handler.request.sendall(response_frame)

        print("")

        sys.stdout.flush()
        sys.stderr.flush()


def constructResponseFrame(dataDict):
    dataDict = json.dumps(dataDict).encode()
    print("Response payload len: " + str(len(dataDict)))
    response_payload_len = len(dataDict)
    response_frame = bytearray()
    prebits = (129).to_bytes(1, "big")
    response_frame += prebits # add fin bit, rsvs bit and opcode

    if response_payload_len < 126:
        response_frame += response_payload_len.to_bytes(1, "big")
    elif response_payload_len >= 126 and response_payload_len < 65536:
        signifier = 126
        response_frame += signifier.to_bytes(1, "big")
        response_frame += response_payload_len.to_bytes(2, "big")
    elif response_payload_len >= 65536:
        signifier = 127
        response_frame += signifier.to_bytes(1, "big")
        response_frame += response_payload_len.to_bytes(8, "big")

    response_frame += dataDict

    return response_frame


def constructResponseFrameFromBytes(dataBytes):
    print("Response payload len(bytes): " + str(len(dataBytes)))
    response_payload_len = len(dataBytes)
    response_frame = bytearray()
    prebits = (129).to_bytes(1, "big")
    response_frame += prebits # add fin bit, rsvs bit and opcode

    if response_payload_len < 126:
        response_frame += response_payload_len.to_bytes(1, "big")
    elif response_payload_len >= 126 and response_payload_len < 65536:
        signifier = 126
        response_frame += signifier.to_bytes(1, "big")
        response_frame += response_payload_len.to_bytes(2, "big")
    elif response_payload_len >= 65536:
        signifier = 127
        response_frame += signifier.to_bytes(1, "big")
        response_frame += response_payload_len.to_bytes(8, "big")

    response_frame += dataBytes

    print("Response frame len(bytes): " + str(len(response_frame)))
    return response_frame


# escape the html txt
def escape_html(input):
    return input.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")


# def getChatHistory(request, handler):
#     chatdata = json.dumps(db.list_chats()).encode()
#     response = generate_response(chatdata, "application/json; charset=utf-8", "200 OK")
#     handler.request.sendall(response)