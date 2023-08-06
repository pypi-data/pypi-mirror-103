import grpc
import sys
import os

p = os.path.abspath(os.path.dirname(__file__))
if p not in sys.path:
    sys.path.append(p)

import user_pb2
import user_pb2_grpc



def run(addr):
    u = User(addr)
    res = u.login()
    return res


class User:
    def __init__(self, addr):
        self.addr = addr

    def login(self) -> user_pb2.LoginResponse:
        channel = grpc.insecure_channel(self.addr)
        stub = user_pb2_grpc.UserStub(channel)
        response = stub.login(user_pb2.LoginRequest(name='you'))
        return response
