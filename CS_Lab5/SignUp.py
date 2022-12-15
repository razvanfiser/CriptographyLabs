import hashlib
import DataBase

class SignUp():
    def __init__(self):
        self.db = DataBase.DataBase()
        self.username = ""
        self.password = ""

    def hash_pass(self):
        self.password = self.password.encode('utf-8')
        return hashlib.sha256(self.password).hexdigest()

    def send_data(self, username, password):
        self.username = username
        self.password = password
        self.password = self.hash_pass()
        self.db.add_entry(self.username, self.password)

    def retrieve_data(self):
        print(self.db.print_all())


