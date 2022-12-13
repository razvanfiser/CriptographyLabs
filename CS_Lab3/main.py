import RSA

PT = "Hello m9 do yuo wanna blaze it"
q, p = 239, 151
e = 277

rsa = RSA.RSA(q, p, e)
encrypted = rsa.encrypt(PT)
print(encrypted)
decrypted = rsa.decrypt(encrypted)
print(decrypted)