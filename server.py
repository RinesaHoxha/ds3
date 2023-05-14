import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 8080
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print('Server listening on {}:{}'.format(self.host, self.port))
        
    def start(self):
        client1, address1 = self.server_socket.accept()
        print('Connection from:', address1)
        
        client2, address2 = self.server_socket.accept()
        print('Connection from:', address2)
        
        # Generate RSA key pair
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()
