from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
from DataBase import DataBase
import json
from CaesarSubstCipher import CaesarSubstCipher
import pyotp
import qrcode
import time
import base64

db = DataBase()

hostName = "localhost"
serverPort = 8080
sessions = {}

class MyServer(BaseHTTPRequestHandler):
    def generate_sess_id(self):
        return "".join([str(item) for item in np.random.randint(0, 10, 100)])

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) \
            if cookie_list else {}

    def do_GET(self):
        routes = {
            "/login": self.login,
            "/register": self.register,
            "/logout": self.logout,
            "/": self.home,
            "/encrypt": self.encrypt,
            "/userlist": self.userlist
        }
        self.cookie = None  # Addition

        if self.path in routes.keys():
            response = 200
            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.user = cookies["sid"] if (cookies["sid"] in sessions) else False
            else:
                self.user = False

            content = routes[self.path]()
        else:
            response = 404
            content = "Not Found"


        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        if self.cookie:
            print("COOKIE!")
            self.send_header('Set-Cookie', self.cookie)  # Addition
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))
        return

    def home(self):
        return "Welcome User!" if self.user else "Welcome Stranger!"

    def encrypt(self):
        content_length = int(self.headers.get('Content-length', 0))
        data = json.loads(self.rfile.read(content_length).decode())
        return CaesarSubstCipher(data["key"]).encrypt_message(data["message"]) if self.user else "Sorry, you need to be logged in to do that!"

    def userlist(self):
        if self.user:
            username = sessions[self.user][0]
            if db.check_role(username):
                return db.print_all()
            else:
                return "Sorry, you need admin privileges for that!"
        else:
            return "Sorry, you need to be Logged In and an Admin to do that!"

    def login(self):
        content_length = int(self.headers.get('Content-length', 0))
        data = json.loads(self.rfile.read(content_length).decode())

        key = base64.b32encode(bytearray(data["username"], 'ascii')).decode('utf-8')
        totp_object = pyotp.TOTP(key)

        if db.is_user_in_db(data["username"], data["password"])[0] and totp_object.verify(data["otp"]):
            sid = self.generate_sess_id()
            self.cookie = "sid={}".format(sid)
            sessions[sid] = [data["username"], "useragent", "ip address", "expiry"]
            return "Logged In"
        else:
            return "Username or Password is Wrong"

    def register(self):
        content_length = int(self.headers.get('Content-length', 0))
        data = json.loads(self.rfile.read(content_length).decode())

        key = base64.b32encode(bytearray(data["username"], 'ascii')).decode('utf-8')
        # uri = pyotp.totp.TOTP(key).provisioning_uri(name=data["username"], issuer_name="Răzvan's Service")
        totp_object = pyotp.TOTP(key)

        # t = time.localtime()
        # current_time = time.strftime("%H_%M_%S_%b_%Y", t)
        # qrcode.make(uri).save("qr_code" + current_time + ".png")

        username, password, role = data["username"], data["password"], "user"
        if not db.is_username_in_db(data["username"]) and totp_object.verify(data["otp"]):
            db.add_entry(username, password, role)
            return "Registered!"
        else:
            return "Username already taken!"


    def logout(self):
        # todo: perform logout
        return "Logged Out"

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")