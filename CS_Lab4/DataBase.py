import sqlite3
class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE users (
                    username text,
                    password text
                    )""")
        self.conn.commit()

    def add_entry(self, username, password):
        self.c.execute("INSERT INTO users VALUES ('{user}', '{passw}')".format(user=username, passw=password))
        self.conn.commit()

    def print_all(self):
        self.c.execute("SELECT * FROM users")
        self.conn.commit()
        return "\n".join([" ".join([str(item) for item in row]) for row in self.c.fetchall()])


