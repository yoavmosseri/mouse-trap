import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

# Generate an RSA key pair
key = RSA.generate(2048)

# Save the public key
public_key = key.publickey()
with open('public_key.pem', 'wb') as f:
    f.write(public_key.export_key())

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 12345)
print(f'Starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    print(f'Connected from {client_address}')

    # Receive encrypted message and AES key from the client
    encrypted_message = connection.recv(1024)
    encrypted_key = connection.recv(1024)

    # Decrypt the AES key
    aes_key = key.decrypt(encrypted_key)

    # Create a new AES cipher object
    cipher = AES.new(aes_key, AES.MODE_ECB)

    # Decrypt the message
    message = cipher.decrypt(encrypted_message)
    print(f'Received message: {message.decode()}')

    # Encrypt response
    encrypted_response = cipher.encrypt(b'ACK')

    # Send the encrypted response back to the client
    connection.sendall(encrypted_response)

    # Clean up the connection
    connection.close()
