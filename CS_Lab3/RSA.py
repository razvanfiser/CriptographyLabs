import math

class RSA():
    def __init__(self, q, p, e):
        self.q = q
        self.p = p
        self.e = e
        self.n = p * q
        self.d = None

    def gcd(self, p, q):
        while q != 0:
            p, q = q, p % q
        return p

    def check_stuff(self):
        A = (self.q - 1) * (self.p - 1)

        if self.e > A:
            print(f"Error. E = {self.e} is bigger than A = {A}.")
            return False

        if not self.gcd(A, self.e) == 1:
            print(f"Error. E = {self.e} and A = {A} are not coprimes")
            return False

        self.d = pow(self.e, -1, A)

        return True

    def to_ascii(self, message):
        return [ord(c) for c in message]

    def encrypt(self, message):
        new_message = self.to_ascii(message)

        if not self.check_stuff():
            return "Error."

        encrypted = []

        # encrypt the message
        for i in new_message:
            pw = i ** self.e
            rem = pw % self.n
            encrypted.append(rem)
        return encrypted

    def decrypt(self, message):
        decoded = ""

        # decode the message
        for i in message:
            pw = i ** self.d
            rem = pw % self.n
            decoded += chr(rem)

        return decoded