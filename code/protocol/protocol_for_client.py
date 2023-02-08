import socket
from tcp_by_size import send_with_size,recv_by_size
from aes import AESCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from dot import Dot
from user import User
from network import Network
import base64
import pickle

class NetC:
    def __init__(self, socket: socket.socket):
        self.sock = socket
        self.admin = False
        self.connected = False
        self.logged_in = False
        self.aes = None


    def __send_encrypted(self, message):
        if self.connected and self.aes is not None:
            send_with_size(self.sock, self.aes.encrypt(message))

    def __recv_decrypted(self):
        if self.connected and self.aes is not None:
            return self.aes.decrypt(recv_by_size(self.sock))


    def connect(self, ip, port) -> bool:
        try:
            self.sock.connect((ip,port))
        except:
            return False
        self.connected = True
        return self.connected
    

    def exchange_keys(self):    
        # send rsa public key
        client_key = RSA.generate(2048)
        message = b"HELLOS~" + client_key.publickey().exportKey()
        send_with_size(self.sock, message)

        # get aes private key
        answer = recv_by_size(self.sock)
        if not answer.split(b'~')[0] == b'HELLOC':
            raise Exception('Wrong message')

        decipher = PKCS1_OAEP.new(client_key)
        key = decipher.decrypt(answer[answer.find(b'~')+1:])
        self.aes = AESCipher(key)

        return True


    def login(self, username: str, password: str) -> bool:
        if '~' in username or '~' in password:
            raise Exception("Wrong input, ~ is not allowed")

        message = f"LOGINA~{username}~{password}"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if not answer.split('~')[0] == 'LOGINR':
            raise Exception('Wrong message')
        
        answer = answer.split('~')[1]
        if answer == 'TRUE':
            self.logged_in = True
        elif answer == 'ADMIN':
            self.logged_in = True
            self.admin = True
        
        return self.logged_in




    def register(self, username: str, password: str, email: str) -> bool:
        if '~' in username or '~' in password or '~' in email:
            raise Exception("Wrong input, ~ is not allowed")

        message = f"REGISA~{username}~{password}~{email}"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if not answer.split('~')[0] == 'REGISR':
            raise Exception('Wrong message')

        if answer.split('~')[1] == 'TRUE':
            return True

        return False
        

    def get_neural_network(self) -> Network:
        message = f"DEFEND"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer.split('~')[0] == 'NOEDAT':
            print("More data is required.")
            return False
        elif answer.split('~')[0] == 'NETREP':
            return pickle.loads(base64.b64decode(answer.split('~')[1]))
        else:
            raise Exception('Wrong message')
            

    def send_mouse_data(self, data: list[Dot]) -> bool:
        pass

    def get_users_list(self) -> list[User]:
        pass

    def remove_user(self, username: str) -> bool:
        pass

    def close(self) -> bool:
        message = f"EXITCL"
        self.__send_encrypted(message)

        answer = self.__recv_decrypted()
        if answer == 'BYECLT':
            print('Bye Bye! :)')

            self.sock.close()
            self.connected = False
        else:
            raise Exception('Wrong message')




client = NetC(socket.socket())

client.connect('127.0.0.1',4444)

client.exchange_keys()


client.register('guy','guy12345','mosseriguy8@gmail.com')

client.login('yoavmosseri','yoav298')

client.close()

