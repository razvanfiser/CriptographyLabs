import requests
from LogIn import LogIn
import hashlib
hostName = "localhost"
serverPort = 8080
address = "http://%s:%s" % (hostName, serverPort)

session = LogIn()
# Register as a person that already is in database, not going to work
session.register("goodguyhimmler1488", "lol123")
print(session.sess_id)

# Requesting Caesar Cipher Encryption Service, not going to work because not logged in
r = requests.get(address + "/encrypt", headers={"Cookie": session.sess_id},
                json={"message": "kektastic", "key": "CDEFGHIJKLMNOPQRSTUVWXYZAB"})
print(r.content)

# Registering as a new user; User receives QR code upon registration to scan with 3rd party Authentificator app
# Then, the Authentificator app will generate valid codes for future LogIns
session.register("razvanfiser", "keklol")
# Logging in as existing user, 2FA consists of entering the correct password and correct code from
# Authentificator app before expiry time (30 s)
session.log_in("razvanfiser", "keklol")
print(session.sess_id)

# Request Caesar Cipher Encryption Service, this is going to work because user is logged in
r = requests.get(address + "/encrypt", headers={"Cookie": session.sess_id},
                json={"message": "kektastic", "key": "CDEFGHIJKLMNOPQRSTUVWXYZAB"})
print(r.content)

# Requesting to access the list of all registered users, not accessible unless admin
# One cannot register as an admin unless they have direct access to the server code
r = requests.get(address + "/userlist", headers={"Cookie": session.sess_id})
print(r.content)

# Log in as an admin account and request list of users
session.log_in("goodguyhimmler1488", "lol123")
r = requests.get(address + "/userlist", headers={"Cookie": session.sess_id})
print(r.content.decode('utf-8'))