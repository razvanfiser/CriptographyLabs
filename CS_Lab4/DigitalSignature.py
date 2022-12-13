import hashlib

class DigitalSignature:
    def __init__(self):
        self.message = ""
        self.digest = ""

    def digest_message(self, message):
        self.message = message
        self.digest = hashlib.sha256(self.message.encode('UTF-8')).hexdigest()
        return self.digest

    def verify_signature(self, dec):
        if self.digest == dec:
            print("Suggess! :DD")
            return True
        return False