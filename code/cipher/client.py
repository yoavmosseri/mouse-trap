import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher.PKCS1_OAEP import AES

# Load the server's public key
with open('public_key.pem', 'rb') as f:
    public_key = RSA.import_key(f.read())

# Create a new AES key
aes_key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'

# Encrypt the AES key with the server's public key
encrypted_key = public_key.encrypt(aes_key, 32)[0]

# Create a new AES cipher object
cipher = AES.new(aes_key, AES.MODE_ECB)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 12345)
print(f'Connecting to {server_address[0]} port {server_address[1]}')
sock.connect(server_address)

try:
    # Encrypt the message
    message = b'Hello, server!'
    encrypted_message = cipher.encrypt(message)

    # Send the encrypted message and encrypted AES key to the server
    sock.sendall(encrypted_message)
    sock.sendall(encrypted_key)

    # Receive the encrypted response from the server
    encrypted_response = sock.recv(1024)

    # Decrypt the response
    response = cipher.decrypt(encrypted_response)
    print(f'Received response: {response.decode()}')

finally:
    # Clean up the connection
    print('Closing socket')
    sock.close()
