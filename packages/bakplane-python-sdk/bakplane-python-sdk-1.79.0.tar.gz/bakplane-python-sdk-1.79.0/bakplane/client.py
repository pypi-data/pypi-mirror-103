import certifi
import grpc

from bakplane.bakplane_pb2_grpc import BakplaneStub


class BakplaneClient(object):
    def __init__(self, address: str, secure: bool = True):
        self.address = address
        self.secure = secure

    def get_connection(self) -> BakplaneStub:
        if not self.secure:
            return BakplaneStub(grpc.insecure_channel(self.address))

        with open(certifi.where(), "rb") as certs:
            credentials = grpc.ssl_channel_credentials(certs.read())
            return BakplaneStub(
                grpc.secure_channel(self.address, credentials=credentials)
            )
