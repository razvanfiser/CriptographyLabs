#  Asymmetric Ciphers.

### Course: Cryptography & Security
### Author: Răzvan Fișer FAF 203

----

## Theory
Asymmetric Cryptography (a.k.a. Public-Key Cryptography)deals with the encryption of plain text when having 2 keys, one being public and the other one private. The keys form a pair and despite being different they are related.

As the name implies, the public key is available to the public but the private one is available only to the authenticated recipients.

A popular use case of the asymmetric encryption is in SSL/TLS certificates along side symmetric encryption mechanisms. It is necessary to use both types of encryption because asymmetric ciphers are computationally expensive, so these are usually used for the communication initiation and key exchange, or sometimes called handshake. The messages after that are encrypted with symmetric ciphers.



Examples: <br>
- RSA
- Diffie-Helman
- ECC
- El Gamal
- DSA

## Objectives:
- Get familiar with the asymmetric cryptography mechanisms.
- Implement an example of an asymmetric cipher.

## Implementation description

## RSA  

Fot starting the algorithm, the user must first choose the 
public key (consists of p, q and e). ```p``` and ```q``` are assumed to be prime, so all that is left is to check some other necessary conditions such as $e > A = (q-1)(p-1)$ and $e$ and $A$ must be coprime, so $gcd(A, e) = 1$. We check these things in the `check_stuff` function:

```py
def check_stuff(self):
    A = (self.q - 1) * (self.p - 1)

    if self.e > A:
        print(f"Error. E = {self.e} is bigger than A = {A}.")
        return False

    if not self.gcd(A, self.e) == 1:
        print(f"Error. E = {self.e} and A = {A} are not coprimes")
        return False

    self.d = pow(self.e, -1, A)
```
To encrypt a message, the plain test must be converted to ASCII.
Each of its elements is taken and raised at the power e. 
``pw = i ** self.e``. Then the result of ``pw % self.n`` is found 
and appended to the encoded string result.


To decrypt a message the same keys must be used, with the only difference
that instead of receiving the public key e as input from the user,
it must receive the private key d. Then the algorithm for obtaining
the decrypted message is the same as for encryption.

## Conclusions / Screenshots / Results
RSA is an algorithm which is used until today. One of its downsides
may be the fact that it is relatively slow, but at the same time it
is hard to break, especially when a large enough key is used.
Its security relies on the computational difficulty of 
factoring large integers.
The implementation of the algorithm works as intended and the
message can be both encrypted and decrypted (if the key is 
already known) correctly.