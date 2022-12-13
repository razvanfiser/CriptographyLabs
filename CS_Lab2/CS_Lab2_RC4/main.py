import RC4

key = "ENCODE THIS TEXT!"
message = "A RANDOM KEY"

rc4 = RC4.RC4(key)
encrypted = rc4.encrypt(message)
print(encrypted)
print("DONE")
decrypted = rc4.decrypt(encrypted)
print(decrypted)
