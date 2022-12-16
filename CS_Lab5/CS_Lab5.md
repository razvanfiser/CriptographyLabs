#  Web Authentication & Authorisation.

### Course: Cryptography & Security
### Author: Răzvan Fișer FAF 203

----

## Theory
Authentication & authorization are 2 of the main security goals of IT systems and should not be used interchangibly. Simply put, during authentication the system verifies the identity of a user or service, and during authorization the system checks the access rights, optionally based on a given user role.

There are multiple types of authentication based on the implementation mechanism or the data provided by the user. Some usual ones would be the following:

- Based on credentials (Username/Password);
- Multi-Factor Authentication (2FA, MFA);
- Based on digital certificates;
- Based on biometrics;
- Based on tokens.

Regarding authorization, the most popular mechanisms are the following:

- Role Based Access Control (RBAC): Base on the role of a user;
- Attribute Based Access Control (ABAC): Based on a characteristic/attribute of a user.


## Objectives:
1. Take what you have at the moment from previous laboratory works and put it in a web service / serveral web services.
2. Your services should have implemented basic authentication and MFA (the authentication factors of your choice).
3. Your web app needs to simulate user authorization and the way you authorise user is also a choice that needs to be done by you.
4. As services that your application could provide, you could use the classical ciphers. Basically the user would like to get access and use the classical ciphers, but they need to authenticate and be authorized.

## Implementation description
The web service implements the basic Register and Login functionalities: Upon registration
it checks wether the username already exists in the database, if it does, it will throw out an error message, else
it will simply add the username and hashed password to the database. Someone who does not
have direct access to the server code cannot register as an admin, but only as a regular
user. When first registering, the user will be provided with a QR Code. They are required to scan it
using a 3rd party Authentificator app and then the Authentificator will provide a new one-time-password
at 30 second intervals which are necessary for further logging in as a registered user. This will
serve as the 2FA for the web service and was implemented using the Python `pyotp` library.

```py
# register function in the MyServer Class within the server file
def register(self):
    content_length = int(self.headers.get('Content-length', 0))
    data = json.loads(self.rfile.read(content_length).decode())

    key = base64.b32encode(bytearray(data["username"], 'ascii')).decode('utf-8')
    totp_object = pyotp.TOTP(key)

    username, password, role = data["username"], data["password"], "user"
    if not db.is_username_in_db(data["username"]) and totp_object.verify(data["otp"]):
        db.add_entry(username, password, role)
        return "Registered!"
    else:
        return "Username already taken!"
```

```py
#  register function from the LogIn class;
def register(self, username, password):
    self.username = username
    self.password = password
    self.password = self.hash_pass()

    key = base64.b32encode(bytearray(self.username, 'ascii')).decode('utf-8')
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=self.username, issuer_name="Răzvan's Service")
    totp_object = pyotp.TOTP(key)

    # here the qr code is sent to the user
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S_%b_%Y", t)
    qrcode.make(uri).save("qr_code" + current_time + ".png")
    print("QR CODE SENT")
    # the first-time one time password is sent to the server
    otp = input("Please scan QR Code using any Authentificator app and insert One Time Password: ")
    r = requests.get(address + "/register", json={"username": username, "password": self.password, "otp": otp})
    print(r.content)
```

When logging in, the server checks whether the username and password (the password is
already hashed by the time it gets to the server) corresponds to the data stored in the server. If so, 
the server sends a <b>session id</b> in the response header back to the user and any
further requests to the server need to contain the session id in order for the user to be 
"remembered". 

```py
def login(self):
    content_length = int(self.headers.get('Content-length', 0))
    data = json.loads(self.rfile.read(content_length).decode())

    key = base64.b32encode(bytearray(data["username"], 'ascii')).decode('utf-8')
    totp_object = pyotp.TOTP(key)

    # check whether credentials are the same as in the database and verify otp
    if db.is_user_in_db(data["username"], data["password"])[0] and totp_object.verify(data["otp"]):
        sid = self.generate_sess_id()
        self.cookie = "sid={}".format(sid)
        sessions[sid] = [data["username"], "useragent", "ip address", "expiry"]
        return "Logged In"
    else:
        return "Username or Password is Wrong"
```
The web service will provide two functions:
* The encryption of a message using the Caesar Cipher (this will require the user to
be logged in);
* The display of all the users who are currently registered (this will require the user to be an
admin).

If the server receives a request at the `/encrypt` route, it will check whether the user is logged in 
based on the existence and the correctness of the session id provided in the 
request headers. Then it will return the encrypted version of the message provided in the
request body.
```py
def encrypt(self):
    content_length = int(self.headers.get('Content-length', 0))
    data = json.loads(self.rfile.read(content_length).decode())
    return CaesarSubstCipher(data["key"]).encrypt_message(data["message"]) if self.user else "Sorry, you need to be logged in to do that!"
```
If the server receives a request at the `/userlist` route, it will check the session id, then
check in the database whether the username corresponding to the id has admin privileges and 
spew out the corresponding output.
```pycon
def userlist(self):
    if self.user:
        username = sessions[self.user][0]
        if db.check_role(username):
            return db.print_all()
        else:
            return "Sorry, you need admin privileges for that!"
    else:
        return "Sorry, you need to be Logged In and an Admin to do that!"
```
## Conclusions
For making a secure app many details should be taken into account, such as: hashing
the password, not allowing unauthorized or unauthenticated users, making sure no one
as access to personal information of another user. 2-Factor-Authentication is
an additional layer of security and neutralizes the risks associated with 
compromised passwords. Authorization grants access to specific resources based on 
an authenticated user's entitlements. In this laboratory work I got to know the basics
of these concepts and everything works as intended.