import RC4

message = "DONT SHOW THIS TO ANYONE"
key = "UMMM OKAY"

rc4 = RC4.RC4(key)
encrypted = rc4.encrypt(message)
print(encrypted)
print("\033[92mENCRYPTION DONE \033[0m")
decrypted = rc4.decrypt(encrypted)
print(decrypted)
