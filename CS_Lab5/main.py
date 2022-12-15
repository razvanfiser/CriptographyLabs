import requests
from LogIn import LogIn
import hashlib
hostName = "localhost"
serverPort = 8080
address = "http://%s:%s" % (hostName, serverPort)

session = LogIn()
# session.register("goodguyhimmler1488", "lol123")
# print(session.sess_id)
#
# r = requests.get(address + "/encrypt", headers={"Cookie": session.sess_id},
#                 json={"message": "kektastic", "key": "CDEFGHIJKLMNOPQRSTUVWXYZAB"})
# print(r.content)

# session.register("razvanfiser", "keklol")
session.log_in("razvanfiser", "keklol")
print(session.sess_id)

r = requests.get(address + "/encrypt", headers={"Cookie": session.sess_id},
                json={"message": "kektastic", "key": "CDEFGHIJKLMNOPQRSTUVWXYZAB"})
print(r.content)

# r = requests.get(address + "/userlist", headers={"Cookie": session.sess_id})
# print(r.content)
#
# session.log_in("goodguyhimmler1488", "lol123")
# r = requests.get(address + "/userlist", headers={"Cookie": session.sess_id})
# print(r.content.decode('utf-8'))