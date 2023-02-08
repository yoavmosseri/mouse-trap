import socket
import threading
from protocol_for_server import NetS
from SQL_ORM import DotORM

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_sock = socket.socket()
        
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(20)

        #next line release the port
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = []
        self.threads = []
        self.db = DotORM()

        print('Server is ready!')


    
    def accept(self):
        while True:
            client, address = self.server_sock.accept()
            print(f"Connected with {str(address)}")
            
            client = NetS(client,DotORM())
            self.clients.append(client)

            thread = threading.Thread(target=client.handle_client)
            self.threads.append(thread)
            thread.start()



server = Server('0.0.0.0',4444)
server.accept()