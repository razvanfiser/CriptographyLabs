import sqlite3
import hashlib

class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username text,
                    password text,
                    role text
                    )""")
        self.conn.commit()
        self.c.execute("INSERT INTO users VALUES (NULL, 'goodguyhimmler1488', '{password}', 'admin')"
                       .format(password=hashlib.sha256("lol123".encode('utf-8')).hexdigest()))
        self.conn.commit()

    def add_entry(self, username, password, role):
        self.c.execute("INSERT INTO users VALUES (NULL, '{user}', '{passw}', '{role}')"
                       .format(user=username, passw=password, role=role))
        self.conn.commit()

    def print_all(self):
        self.c.execute("SELECT * FROM users")
        self.conn.commit()
        return "\n".join([" ".join([str(item) for item in row]) for row in self.c.fetchall()])

    def is_user_in_db(self, username, password):
        self.c.execute("SELECT * FROM users WHERE username='{user}' AND password='{passw}'".format(user=username, passw=password))
        self.conn.commit()
        result = self.c.fetchone()
        if result:
            return True, result
        else:
            return False, False

    def is_username_in_db(self, username):
        self.c.execute(
            "SELECT * FROM users WHERE username='{user}'".format(user=username))
        self.conn.commit()
        result = self.c.fetchone()
        if result:
            return True
        else:
            return False

    def check_role(self, username):
        self.c.execute(
            "SELECT * FROM users WHERE username='{user}' AND role='admin'".format(user=username))
        self.conn.commit()
        result = self.c.fetchone()
        if result:
            return True
        else:
            return False
