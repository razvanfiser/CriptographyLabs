import SignUp
import DigitalSignature
import RSA

data = [("razvanfiser1488", "youstupidmonkey"),
        ("lmfao420blazeit", "letmeinniBBa"),
        ("not_a_glowie", "ilovediversity69")]

sign_up = SignUp.SignUp()

for user, password in data:
    sign_up.send_data(user, password)

sign_up.retrieve_data()

message = "this is my signature"
digital_sig = DigitalSignature.DigitalSignature()
digest = digital_sig.digest_message(message)

rsa = RSA.RSA(239, 151, 277)
encrypted_digest = rsa.encrypt(digest)

decrypted_digest = rsa.decrypt(encrypted_digest)

print(digital_sig.verify_signature(decrypted_digest))


