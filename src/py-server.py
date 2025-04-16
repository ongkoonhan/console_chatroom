#!/usr/bin/python3

import message_pb2
from MessageHandler import MessageHandler

import socket
import threading


PORT = 1111



addrinfo = socket.getaddrinfo(None, PORT, family=socket.AF_INET, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE)
for (family, socktype, proto, canonname, sockaddr) in addrinfo:
    serversocket = socket.socket(family, socktype, proto)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # reuse localhost address for bind()
    serversocket.bind(sockaddr)
    serversocket.listen(5)    
    break


# def client_thread(clientsocket, address):
#     msg = message_pb2.MsgTCP()
#     # recv
#     chunk = clientsocket.recv(1024)
#     print(chunk)
#     size = socket.ntohl(int.from_bytes(chunk[:4], "big"))   # 32 bit msg size in network byte order
#     print(f"size: {size}")
#     msg.ParseFromString(chunk[4:])
#     print(msg)
#     # send
#     msg.msg = "msg accepted"
#     serialized = msg.SerializeToString()
#     clientsocket.send(serialized)
#     clientsocket.close()
#     print("exit thread")


def client_thread(clientsocket, address):
    message_handler = MessageHandler(clientsocket)
    msg = message_handler.recv_proto_msg()   # blocking
    if msg.msg_type == message_pb2.MsgType.MSG_TCP:
        print(f"tcp msg received")
        print(msg)
        msg.Clear()   # reuse Msg
        msg.id = 22
        msg.msg_type = message_pb2.MsgType.MSG_TCP
        msg.msg_tcp.msg = "your test msg has been received"
        print(f"sending: {msg}")
        message_handler.send_proto_msg(msg)   # blocking
    else:
        print(f"unknown msg received")
    clientsocket.close()
    print("exit thread")


threads = []
while True:
    (clientsocket, address) = serversocket.accept()   # blocking
    t = threading.Thread(target=client_thread, args=(clientsocket, address))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


serversocket.close()







# TODO: handle loop for send() and recv()
#       create msg parsing loop for size + msg bytes