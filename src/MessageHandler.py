import message_pb2

import socket


RECV_SIZE = 1024
MSG_SIZE_SIZE = 4   # 32-bit uint (4 bytes)


class MessageHandler:

    def __init__(self, socket_):
        self.__socket = socket_


    def log(self, str_) -> None:
        print(f"MessageHandler: {str_}")


    ### client/server protocol
    #   on every send, an ack is expected to be received
    #   on every recv, an ack is expected to be sent
    #   the ack id matches the send/recv msg id

    def recv_proto_msg(self) -> message_pb2.Msg:
        # recv proto msg
        msg = message_pb2.Msg()        
        serialized = self.__recv_loop()   # blocking
        msg.ParseFromString(serialized)
        if self.__check_tcp_msg(msg.msg_type):
            self.__send_ack(msg.id)   # ack only if valid proto msg
            return msg
        else:
            return None


    def send_proto_msg(self, proto_msg) -> bool:
        # send only if valid proto msg
        if self.__check_tcp_msg(proto_msg.msg_type):
            # send proto msg
            serialized = proto_msg.SerializeToString()
            self.__send_loop(serialized, proto_msg.ByteSize())   # blocking
            id_ = proto_msg.id
            # wait for ack
            ack = message_pb2.Msg()
            serialized = self.__recv_loop()   # blocking
            ack.ParseFromString(serialized)
            return ack.msg_type == message_pb2.MsgType.ACK_TCP and ack.id == id_
        else:
            return False


    ### simple proto msg send/recv protocol
    #   send/recv packet format consists of [ proto msg size, proto msg ] 
    #   proto msg size is fixed as a 32-bit uint (4 bytes)
    #   proto msg is serialized as bytes
    #   when the proto msg is larger than the recv buffer size (RECV_SIZE), the 
    #       proto msg size is used to ensure that the full proto msg is received

    def __recv_loop(self) -> bytes:
        chunks = []
        chunk = self.__socket.recv(RECV_SIZE)
        size = self.__decode_size(chunk[:MSG_SIZE_SIZE])   # get size of proto msg
        size_received = len(chunk) - MSG_SIZE_SIZE
        chunks.append(chunk[MSG_SIZE_SIZE:])
        while size_received < size:
            chunk = self.__socket.recv(RECV_SIZE)
            chunks.append(chunk)
            size_received += len(chunk)
        self.log(f"__recv_loop().size_received: {size_received + MSG_SIZE_SIZE}")
        return b"".join(chunks)


    def __send_loop(self, bytes_, size) -> None:
        bytes_ = b"".join([self.__encode_size(size), bytes_])   # send size + msg payload
        size_sent = 0
        while size_sent < size:
            size_sent += self.__socket.send(bytes_[size_sent:])   # not all bytes might be send on every call
        self.log(f"__send_loop().size_sent: {size_sent}")

    
    ### utilities

    def __send_ack(self, msg_id) -> None:
        msg = message_pb2.Msg()
        msg.id = msg_id
        msg.msg_type = message_pb2.MsgType.ACK_TCP
        serialized = msg.SerializeToString()
        self.__send_loop(serialized, msg.ByteSize())   # blocking


    def __encode_size(self, int_) -> bytes:
        return socket.htonl(int_).to_bytes(MSG_SIZE_SIZE, "big")    # 32 bit msg size in network byte order


    def __decode_size(self, bytes_) -> int:
        return socket.ntohl(int.from_bytes(bytes_, "big"))   # 32 bit msg size in network byte order


    def __check_tcp_msg(self, msg_type_enum) -> bool:
        return msg_type_enum == message_pb2.MsgType.MSG_TCP \
            or msg_type_enum == message_pb2.MsgType.LOGIN_TCP

