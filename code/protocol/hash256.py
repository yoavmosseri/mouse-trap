import hashlib

class hash:
    def sha265(string: str):
        return hashlib.sha256(string.encode()).hexdigest()


