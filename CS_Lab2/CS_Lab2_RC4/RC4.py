import numpy as np

class RC4():
    def __init__(self, key):
        self.S = np.arange(0, 256)
        self.key = [ord(char) for char in key]

    def key_scheduling(self):
        j = 0

        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[[i, j]] = self.S[[j, i]]

    def key_stream(self):
        i = 0
        j = 0
        while True:
            i = (1 + i) % 256
            j = (self.S[i] + j) % 256
            self.S[[i, j]] = self.S[[j, i]]

            # After reaching S[255] the process continues, starting from S[0] again
            yield self.S[(self.S[i] + self.S[j]) % 256]

    def encrypt(self, message):

        # Converting chars to ascii
        PT = [ord(char) for char in message]
        key = self.key

        self.key_scheduling()
        ks = self.key_stream()

        result = ''
        for c in PT:
            xor = c ^ next(ks)
            add = str(hex(xor))
            result += add

        # returning the result
        return result

    def decrypt(self, message):
        # converting the message from hex to decimal
        encoded = message.split('0x')[1:]
        encoded = [int('0x' + c.lower(), 0) for c in encoded]

        # Converting chars to ascii
        key = self.key

        # calling the key scheduling algorithm
        self.key_scheduling()

        # Stream Generation
        ks = self.key_stream()

        result = ''

        # decrypting the message using xor, just as in case of encryption. This time using the encoded message
        for c in encoded:
            dec = str(chr(c ^ next(ks)))
            result += dec

        return result