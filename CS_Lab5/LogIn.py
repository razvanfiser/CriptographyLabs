import hashlib
import requests
import DataBase
from CaesarSubstCipher import CaesarSubstCipher
import pyotp
import time
import qrcode
import base64

hostName = "localhost"
serverPort = 8080
address = "http://%s:%s" % (hostName, serverPort)

class LogIn():
    def __init__(self):
        self.db = DataBase.DataBase()
        self.username = ""
        self.password = ""
        self.sess_id = ""

    def hash_pass(self):
        self.password = self.password.encode('utf-8')
        return hashlib.sha256(self.password).hexdigest()

    def log_in(self, username, password):
        self.username = username
        self.password = password
        self.password = self.hash_pass() # dont forget to hash it l8r
        otp = input("Please insert One Time Password: ")
        r = requests.get(address + "/login", json={"username": username, "password": self.password, "otp": otp})
        print(r.content)
        try:
            self.sess_id = r.headers["Set-Cookie"]
        except (KeyError):
            pass
        # print(self.sess_id)

    def register(self, username, password):
        self.username = username
        self.password = password
        self.password = self.hash_pass()

        key = base64.b32encode(bytearray(self.username, 'ascii')).decode('utf-8')
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=self.username, issuer_name="Răzvan's Service")
        totp_object = pyotp.TOTP(key)

        t = time.localtime()
        current_time = time.strftime("%H_%M_%S_%b_%Y", t)
        qrcode.make(uri).save("qr_code" + current_time + ".png")
        print("QR CODE SENT")

        otp = input("Please scan QR Code using any Authentificator app and insert One Time Password: ")
        r = requests.get(address + "/register", json={"username": username, "password": self.password, "otp": otp})
        print(r.content)

    # def request_caesar(self):



