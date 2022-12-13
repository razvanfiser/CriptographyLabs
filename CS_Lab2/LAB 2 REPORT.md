#  Symmetric Ciphers. Stream Ciphers. Block Ciphers.

### Course: Cryptography & Security
### Author: Răzvan Fișer FAF 203

----

## Theory
Symmetric Cryptography deals with the encryption of plain text when 
having only one encryption key which needs to remain private. 
Based on the way the plain text is processed/encrypted there 
are 2 types of ciphers:

Stream ciphers: <br>
- The encryption is done one byte at a time.
- Stream ciphers use confusion to hide the plain text.
- Make use of substitution techniques to modify the plain text.
- The implementation is fairly complex.
- The execution is fast.

Block ciphers:
- The encryption is done one block of plain text at a time.
- Block ciphers use confusion and diffusion to hide the plain text.
- Make use of transposition techniques to modify the plain text.
- The implementation is simpler relative to the stream ciphers.
- The execution is slow compared to the stream ciphers.

Some examples of stream ciphers are the following:
- Grain
- HC-256
- PANAMA
- Rabbit
- Rivest Cipher (RC4): It uses 64 or 128-bit long keys. It is used in TLS/SSL and IEEE 802.11 WLAN.
- Salsa20 
- Software-optimized Encryption Algorithm (SEAL)
- Scream 

The block ciphers may differ in the block size which is a 
parameter that might be implementation specific. Here are some 
examples of such ciphers:

- 3DES
- Advanced Encryption Standard (AES): A cipher with 128-bit block 
length which uses 128, 192 or 256-bit symmetric key.
- Blowfish
- Data Encryption Standard (DES): A 56-bit symmetric key cipher.
- Serpent
- Twofish: A standard that uses Feistel networks. It uses blocks 
of 128 bits with key sizes from 128-bit to 256-bit.

## Objectives:
- Get familiar with the symmetric cryptography, stream and block ciphers.
- Implement an example of a stream cipher.
- Implement an example of a block cipher.
- The implementation should, ideally follow the abstraction/contract/interface used in the previous laboratory work.
- Please use packages/directories to logically split the files that you will have.
- As in the previous task, please use a client class or test classes to showcase the execution of your programs


## Implementation description

## 1. Stream Cipher: RC4
### Encryption
RC4 is a stream cipher and variable-length key algorithm. This algorithm 
encrypts one byte at a time (or larger units at a time). A key input is 
pseudorandom bit generator that produces a stream 8-bit number that is 
unpredictable without knowledge of input key, The output of the generator 
is called key-stream, is combined one byte at a time with the plaintext 
stream cipher using X-OR operation.

To encrypt a message, the function ```encrypt``` receives the plain text and 
the key as input from the user and converts them to ascii. Then the key scheduling
algorithm is called which initializes a permutation in array```S``, which has
length = 256 and initially contains integers from 0 to 255 in ascending order.

```py
def key_scheduling(self):
    j = 0

    for i in range(256):
        j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
        self.S[[i, j]] = self.S[[j, i]]
```

After performing the first step, vector S is initialized so there is no need to
use the initial key anymore. The second step is to generate a key stream (also 
called Stream Generation). Each S[i] is swapped with another byte in S according 
to a scheme dictated by the current configuration of S.

```py
def key_stream(self):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (self.S[i] + j) % 256
        self.S[[i, j]] = self.S[[j, i]]

        # After reaching S[255] the process continues, starting from S[0] again
        yield self.S[(self.S[i] + self.S[j]) % 256]
```

To encrypt a message, each ascii value from the plain text array must be xored
with each next value produced by the function ```key_stream``` and the hex
value of the result is added to a string named result, which contains the 
encrypted result.


The function ```decrypt``` receives the encoded message and key from the user.
After it converts the encoded message from hex to decimal and the key to ascii,
the same algorithms for key scheduling and stream generation as for encryption are 
called. Then the message is decrypted using xor, just as in the previous example,
but this time using the encoded message.


## 1. Block Cipher: DES
The Data Encryption Standard (DES) is a symmetric-key block cipher published by 
the National Institute of Standards and Technology (NIST). It is based on the two fundamental attributes of cryptography: substitution 
and transposition. DES consists of 16 steps, each of which is called a round.

The function `step_2` from the `DES` class is the function that de facto implements the algorithm, the `encrypt` function deals with padding and slicing the input messsage into 64-bit slices.
<!-- The function ```encrypt``` receives the plain text (```PT```) and key from the user.
It then converts the PT to hex and splits it into chunks of 16 characters. Using the
binary representation of the key, the function ```key_processing``` is called
which makes permutation of the key according to the PC1 table and splits it in 
left and right parts C0 and D0. A left shift algorithm is performed on C0 and 0D and
this way we obtain arrays C and D each with 17 variants of the left and right key.
17 keys K are obtained by adding the halves together, then permutations are performed
on K according to the PC2 table. After all these steps, a new key ```KEY_PC2``` was obtained. -->
```py
def step_2(self, message):
    K = self.obtain_subkeys()
    M_IP = self.permute(message, self.IP)
    L_0, R_0 = self.split(M_IP)
    L, R = [L_0], [R_0]

    for i in range(16):
        L.append(R[i])
        R.append(self.xor(L[i], self.f(R[i], K[i])))
    R16L16 = R[16] + L[16]
    return self.permute(R16L16, self.IP_inverse)
```
The `step_2` method first calls `self.obtain_subkeys()`, which will first apply the `PC1` table unto the initial key to obtain $C_0$ and $D_0$, then apply shifts to get all 16 $C_n$ and $D_n$ blocks, where $n \in \{1...16\}$. Then table `PC2` is applied to get blocks $K_n$.

```py
def obtain_C_D(self):
    shifts = [1] * 2 + [2] * 6 + [1] + [2] * 6 + [1]
    K_plus = self.permute(self.K, self.PC_1)
    C_0, D_0 = self.split(K_plus)
    C = [C_0]
    D = [D_0]
    for i in range(len(shifts)):
        C.append(self.shift(C[i], shifts[i]))
        D.append(self.shift(D[i], shifts[i]))
    return C, D

def obtain_subkeys(self):
    C, D = self.obtain_C_D()
    return [self.permute(C[i] + D[i], t.PC_2) for i in range(1, 17)]
```
Then an initial permutation is applied to the message $M$ by applying the $IP$ table then $L_0$ and $R_0$ are obtained by splitting the resulting `M_IP` block. The remaining 16 $L_n$ and $R_n$ blocks are obtained by recursively applying the properties:

$$
L[i] = R[i-1]\\
R[i] = L[i-1]\ XOR\ f(R[i-1]K[i])
$$
All that is left is to define the function $f$, which is implemented below:

```py
    def f(self, a, b):
        R, K = a, b
        E_R = self.permute(R, self.E_bit)
        E_R_xor_K = self.xor(E_R, K)
        B = [E_R_xor_K[i:i+6] for i in range(0, len(E_R_xor_K), 6)]
        S_box_out = []
        for ind in range(8):
            b = B[ind]
            i, j = 2*int(b[0]) + int(b[-1]), 8 * int(b[1]) + 4 * int(b[2]) + 2 * int(b[3]) + 1 * int(b[4])
            S_box_out.append( '{:04b}'.format(self.S[ind][i, j]) )
        S_box_out = "".join(S_box_out)
        out = self.permute(S_box_out, self.P)
        return out
```
The proces of Decryption is the same as the process for Encryption, but instead of
using the normal key KEY_PC2 obtained after the key_processing function is called,
the algorithm uses it in reverse order. 
```K = self.obtain_subkeys()[::-1]```

## Conclusions / Screenshots / Results
RC4 is a simple and fast cypher but at the same time not secure. The keystream 
generated by the RC4 is biased to varying degrees towards certain sequences which
makes it even more vulnerable. DES is more secure than RC4 and the most practical 
attack which can be used in order to break it is a brute-force attack. The biggest
downside of it is the relatively short 56-bit key size.
The objectives of this laboratory work were accomplished. Everything works as 
intended.