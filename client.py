import socket
import threading
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_key = None
        self.server_key = None
        self.username = None

    def start(self):
        self.client_socket.connect((self.host, self.port))

        # Generate RSA key pair for client
        self.client_key = RSA.generate(2048)

        # Send client's public key to server
        self.client_socket.send(self.client_key.publickey().exportKey())

        # Receive server's public key
        self.server_key = RSA.importKey(self.client_socket.recv(1024))

        # Get username from user input
        self.username = input("Enter your username: ")

        # Send username to server encrypted with server's public key
        username_cipher = PKCS1_OAEP.new(self.server_key)
        self.client_socket.send(username_cipher.encrypt(self.username.encode()))

        # Start separate thread to listen for incoming messages from server
        threading.Thread(target=self.receive_messages).start()

        # Loop to get user input and send messages to server
        while True:
            message = input()
            if message.lower() == "exit":
                self.client_socket.close()
                sys.exit(0)
            message_cipher = PKCS1_OAEP.new(self.server_key)
            self.client_socket.send(message_cipher.encrypt(message.encode()))

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(4096)
            message_cipher = PKCS1_OAEP.new(self.client_key)
            message = message_cipher.decrypt(message).decode()
            print(message)

if __name__ == "__main__":
    client = Client("localhost", 8080)
    client.start()

