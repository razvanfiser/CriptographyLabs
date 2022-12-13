#  Hash functions and Digital Signatures.

### Course: Cryptography & Security
### Author: Răzvan Fișer FAF 203

----

## Theory
Hashing is a technique used to compute a new representation of an existing value, message or any piece of text. The new representation is also commonly called a digest of the initial text, and it is a one way function meaning that it should be impossible to retrieve the initial content from the digest.

Such a technique has the following usages:

- Offering confidentiality when storing passwords,
- Checking for integrity for some downloaded files or content,
- Creation of digital signatures, which provides integrity and non-repudiation. 
- In order to create digital signatures, the initial message or text needs to be hashed to get the digest. After that, the digest is to be encrypted using a public key encryption cipher. Having this, the obtained digital signature can be decrypted with the public key and the hash can be compared with an additional hash computed from the received message to check the integrity of it.

### Examples
- Argon2
- BCrypt
- MD5 (Deprecated due to collisions)
- RipeMD
- SHA256 (And other variations of SHA)
- Whirlpool


## Objectives:
1. Get familiar with the hashing techniques/algorithms. 
2. Use an appropriate hashing algorithms to store passwords in a local DB. 

   1. You can use already implemented algortihms from libraries provided for your language. 
   2. The DB choise is up to you, but it can be something simple, like an in memory one.

3. Use an asymmetric cipher to implement a digital signature process for a user message.
   1. Take the user input message. 
   2. Preprocess the message, if needed. 
   3. Get a digest of it via hashing. 
   4. Encrypt it with the chosen cipher. 
   5. Perform a digital signature check by comparing the hash of the message with the decrypted one.

## Implementation description
The first thing that happens is connecting to a in-memory database and creating a 
table named user with 2 fields: username and password. Then the authorisation 
process is initialized. The user must write his/her username and password, then the
password is encoded to UTF-8 and with the help of hashlib library and the algorithm
<b>sha256</b> the digest of the password is obtained and both the username and password
are added to the database through the functions implemented in the `SignUp` class.
```py
class SignUp():
    def __init__(self):
        self.db = DataBase.DataBase()
        self.username = ""
        self.password = ""

    def hash_pass(self):
        self.password = self.password.encode('utf-8')
        return hashlib.sha256(self.password).hexdigest()

    def send_data(self, username, password):
        self.username = username
        self.password = password
        self.password = self.hash_pass()
        self.db.add_entry(self.username, self.password)

    def retrieve_data(self):
        print(self.db.print_all())
```
In order to verify the digital signature first, the user must write a message. It goes through some pre-processing and is 
encoded to UTF-8, thed a digest of the message is obtained with the help of sha256
algorithm. The digest is then encoded with the help of RSA algorithm and the result
after encoding is decoded. The signature is verified by comparing the result after 
digest and before encryption with the result after decryption. If the values coincide,
then the digital signature was verified successfully.
```py
class DigitalSignature:
    def __init__(self):
        self.message = ""
        self.digest = ""

    def digest_message(self, message):
        self.message = message
        self.digest = hashlib.sha256(self.message.encode('UTF-8')).hexdigest()
        return self.digest

    def verify_signature(self, dec):
        if self.digest == dec:
            print("Suggess! :DD")
            return True
        return False
```

## Conclusions / Screenshots / Results
Hashing is good to compare two files for equality. 
Without comparing 2 files word-for-word, their hash value may be compared. 
In other words, it checks if the data is copied correctly between two resources.
Hashing passwords before storing them in a database is a good practice because
if a hacker gets access to the database he will not have access to your real password.
At the same time, the integrity of your password sent during login will be
verified against the stored hash.
In this laboratory works task the sha256 algorithm was use for hashing, sqlite as a 
database and the RSA algorithm for encryption and decryption. Everything works as intended - 
the hashed password is stored inside a database along with a username, and the verification
of digital signature is successful.