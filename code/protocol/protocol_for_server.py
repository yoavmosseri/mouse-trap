import socket
from tcp_by_size import send_with_size,recv_by_size
from aes import AESCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
from SQL_ORM import DotORM
from hash256 import hash
from user import User

class NetS:
    def __init__(self, socket: socket.socket, db: DotORM):
        self.db = db
        self.sock = socket
        self.connected = True
        self.logged_in = False
        self.admin = False
        self.aes = None

    def __send_encrypted(self, message):
        if self.connected and self.aes is not None:
            send_with_size(self.sock, self.aes.encrypt(message))

    def __recv_decrypted(self):
        if self.connected and self.aes is not None:
            return self.aes.decrypt(recv_by_size(self.sock))

    
    def __generate_key(self,length=16):
        return os.urandom(length)

    def handle_client(self):
        to_exit = False

        while not self.exchange_keys():
            print('Encryption is not set yet.')
        
        while not to_exit:
            message = self.__recv_decrypted()
            code, fields = message.split('~')[0], message.split('~')[1:]

            answer = self.protocol_build_reply(code,fields)

            if answer is not None:
                self.__send_encrypted(answer)

            if code == 'EXITCL':
                to_exit = True


    def protocol_build_reply(self, code, fields):
        if code == 'LOGINA':
            answer = self.check_login_attempt(fields[0],fields[1])
        elif code == 'REGISA':
            answer = self.create_new_account(fields[0],fields[1],fields[2])
        elif code == 'DEFEND':
            answer = self.get_neural_network()


        elif code == 'EXITCL':
            answer = self.exit()
        else:
            answer = 'SRVERR~Unknown request..'

        return answer

    def get_neural_network(self):
        


    def exit(self):
        return 'BYECLT'
    
    def create_new_account(self, username: str, password: str, email: str) -> bool:
        new_user = User(username,password,email)
        success = 'FALSE'
        try:
            if self.db.insert_user(new_user):
                success = 'TRUE'
        except:
            pass

        return f'REGISR~{success}'


    def check_login_attempt(self, username: str, password: str) -> str:
        print(f"trying to login with: {username}, {password}")
        login = ""
        correct_hash = self.db.get_user_password(username)
        if correct_hash != False:
            current_hash = hash.sha265(password)

            if current_hash == correct_hash:
                admin = self.db.is_admin(username)
                self.admin = admin

                login = 'ADMIN' if admin else 'TRUE'
                self.logged_in = True
                self.id = self.db.get_id(username)
        if login == "":
            login = "FALSE"
        
        return f"LOGINR~{login}"


        
        
        

    def exchange_keys(self):
        message = recv_by_size(self.sock)
        if not message.split(b'~')[0] == b'HELLOS':
            raise Exception('Wrong message')
        
        client_public_key = RSA.importKey(message.split(b'~')[1])

        key = self.__generate_key()

        cipher = PKCS1_OAEP.new(client_public_key)
        encrypted_key = cipher.encrypt(key)
        send_with_size(self.sock,b'HELLOC~'+encrypted_key)

        self.aes = AESCipher(key)

        return True



