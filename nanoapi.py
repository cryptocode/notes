import core_pb2 as types
import socket
import sys
import struct
import time
from google.protobuf.json_format import MessageToJson
import google.protobuf.descriptor_pb2

class API:
    def __init__(self, conn):
        self.conn = conn

    def query(self, query_object):
        typename = type(query_object).__name__
        res = self.conn.send_query(eval('types.'+typename[6:].upper()), query_object)
        res_obj = eval('types.res_' + typename[6:].lower() + '()')
        res_obj.ParseFromString(res)
        return res_obj

    def to_json(self, obj):
        return MessageToJson(obj)

class SocketConnection:
    """TCP or domain socket connection to the IPC server"""
    def __init__(self, address): 
        self.address = address
        print >>sys.stdout, 'Connecting to node at %s' % self.address
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.address)
        except socket.error, msg:
            print >>sys.stderr, msg
            sys.exit(1)    

    def close (self):
        self.sock.close()

    def send_query(self, query_type, query):
        header = types.query()
        header.type = query_type
        str_header = header.SerializeToString()
        str_query = query.SerializeToString()

        # <i is little endian 32-bit
        packed_heading = struct.pack("<i%ds" % (len(str_header),), len(str_header), str_header)
        packed_query = struct.pack("<i%ds" % (len(str_query),), len(str_query), str_query)
        self.sock.sendall(packed_heading)
        self.sock.sendall(packed_query)

        # Get response header
        response_buf = ''
        while len(response_buf) < 4:
            response_buf += self.sock.recv(1)
        header_len = struct.unpack('<i', response_buf[:4])[0]

        response_buf = ''
        while len(response_buf) < header_len:
            response_buf += self.sock.recv(1)

        response = types.response();
        response.ParseFromString(response_buf);

        # Get response
        response_buf = ''
        while len(response_buf) < 4:
            response_buf += self.sock.recv(1)
        header_len = struct.unpack('<i', response_buf[:4])[0]

        response_buf = ''
        while len(response_buf) < header_len:
            response_buf += self.sock.recv(1)
        return response_buf
