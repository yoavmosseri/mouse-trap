import hashlib

class User():
    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.email = email

