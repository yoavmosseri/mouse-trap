__author__ = 'Itamar'
import base64
from Crypto.Cipher import AES
from Crypto import Random
# Note: Install PyCrypto ('pip install crypto')
# Also might want to save iv.

BS = 16
def pad(s): return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
def unpad(s): return s[:-ord(s[len(s)-1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        raw = raw.encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode()


def main():
    text = 'DJ Yossi on the beat!'
    print(text)
    # Encryption
    Encryptor = AESCipher(b'0xF123456789ABAB')
    enc_text = Encryptor.encrypt(text)
    print(enc_text)
    # Decryption
    dec_text = Encryptor.decrypt(enc_text)
    print(dec_text)


if __name__ == '__main__':
    main()
