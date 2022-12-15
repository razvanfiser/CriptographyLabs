class CaesarSubstCipher():
    def __init__(self, substitution_key):
        self.substitution_key = substitution_key
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def encrypt_message(self, raw_message):
        return "".join(
            [self.substitution_key[self.alphabet.index(raw_message[i].upper())] for i in range(len(raw_message))])

    def decrypt_message(self, encrypted_message):
        return "".join([self.alphabet[self.substitution_key.index(encrypted_message[i].upper())] for i in
                        range(len(encrypted_message))])