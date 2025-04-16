#!/usr/bin/python3

import message_pb2
from MessageHandler import MessageHandler

import socket


PORT = 1111



addrinfo = socket.getaddrinfo("localhost", PORT, family=socket.AF_INET, type=socket.SOCK_STREAM)
for (family, socktype, proto, canonname, sockaddr) in addrinfo:
    clientsocket = socket.socket(family, socktype, proto)
    clientsocket.connect(sockaddr)
    break


message_handler = MessageHandler(clientsocket)

msg = message_pb2.Msg()
msg.id = 10
msg.msg_type = message_pb2.MsgType.MSG_TCP
# msg.msg_tcp.msg = "hi this is a test msg"
msg.msg_tcp.msg = "".join([ "hi this is a very long test msg: ", "hi_" * 1000 ])

print(f"sending: {msg}")
message_handler.send_proto_msg(msg)   # blocking

msg = message_handler.recv_proto_msg()   # blocking
print(msg)




# msg = message_pb2.MsgTCP()
# # send
# msg.msg = "hi this is a test msg"
# serialized = msg.SerializeToString()
# size = socket.htonl(msg.ByteSize()).to_bytes(4, "big")    # 32 bit msg size in network byte order
# print(f"size: {msg.ByteSize()}")
# clientsocket.send(b"".join([size, serialized]))   # send size + msg
# # recv
# chunk = clientsocket.recv(1024)
# print(chunk)
# msg.ParseFromString(chunk)
# print(msg)



clientsocket.close()






# TODO: handle loop for send() and recv()
#       (how to handle variable data length?)
