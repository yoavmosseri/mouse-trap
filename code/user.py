#from hash256 import hash

class User():
    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = hash.sha256(password)
        self.email = email

