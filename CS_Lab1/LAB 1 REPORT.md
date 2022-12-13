# Intro to Cryptography. Classical ciphers. Caesar cipher.

### Course: Cryptography & Security
### Author: Răzvan Fișer FAF 203

----

## Theory
 Cryptography consists a part of the science known as Cryptology. The other part is Cryptanalysis. There are a lot of different algorithms/mechanisms used in Cryptography.
 Some of them, which are implemented in this laboratory work are:
- Caesar cipher with one key used for substitution (as explained above);
- Caesar cipher with one key used for substitution, and a permutation of the alphabet;
- Vigenere cipher;
- Playfair cipher.
These are classical ciphers. In contrast to modern cryptographic algorithms, most classical ciphers can be practically computed and solved by hand. However, they are also usually very simple to break with modern technology.


## Objectives:

* Get familiar with the basics of cryptography and classical ciphers.
* Implement 4 types of the classical ciphers:

- Caesar cipher with one key used for substitution (as explained above),
- Caesar cipher with one key used for substitution, and a permutation of the alphabet,
- Vigenere cipher,
- Playfair cipher.


## Implementation description
This laboratory contains the implementation of 4 different algorithms, separated in four different classes, all placed in a .ipynb file (Jupyter Source File), which allows one to run the code in "blocks" rather than one by one, although variables, functions and classes are remembered from block to block.

## Imports
For this project we are going to use the following python libraries: `math` and `numpy`. The first contains useful math-related functions and the second contains functions which make matrix manipulation easier.
```py
import math
import numpy as np
```

## 1. Caesar cipher with one key used for substitution
The `CaesarSubstCipher` class contains two functions: `encrypt_message` and `decrypt_message`. `encrypt_message` finds takes in the plain text message and reads it letter by letter, finds the index of each letter in the alphabet and uses that index to access the corresponding character in the substitution key, which is contained within the `self.subtitution_key` field.
```py
class CaesarSubstCipher():
    def __init__(self, substitution_key):
        self.substitution_key = substitution_key
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    def encrypt_message(self, raw_message):
        return "".join([self.substitution_key[self.alphabet.index(raw_message[i].upper())] for i in range(len(raw_message))])
    
    def decrypt_message(self, encrypted_message):
        return "".join([self.alphabet[self.substitution_key.index(encrypted_message[i].upper())] for i in range(len(encrypted_message))])
```
The function `encrypt_message` uses the same principle, but switches the alphabet and encryption key. Below we can see an implementation of the class defined earlier:
```py
message = "HELLOBEAUTIFULPERSON"
subst_cipher = CaesarSubstCipher("EFGHIJKLMNOPQRSTUVWXYZABCD")
encrypted_message = subst_cipher.encrypt_message(message)
print(encrypted_message)
# This will output 'LIPPSFIEYXMJYPTIVWSR'

decrypted_message = subst_cipher.decrypt_message(encrypted_message)
print(decrypted_message)
# This will output: 'HELLOBEAUTIFULPERSON'
```
Since the final output of encrypting and then decrypting the message is the same as the initial plain text that was given as input, we can be quite certain that the implementation was done correctly.

## 2. Caesar Permutation Cipher
The `CaesarPermutationCipher` implements an additional step of applying a permutation amongst every `n` characters. For example if `n = 5`, every 5 characters will switch places among themselves according to a permutation key. It is not important in which order we apply the subtitution and the permutation for both encryption and decryption.

```py
class CaesarPermutationCipher():
    def __init__(self, substitution_key, permutation_key):
        self.substitution_key = substitution_key
        self.permutation_key = [int(character) for character in permutation_key]
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
    def _pad_message(self, message):
        if len(message) % len(self.permutation_key) != 0:
            return message + "X" * (len(self.permutation_key) - (len(message) % len(self.permutation_key)))
        else:
            return message
    
    def _permute_message(self, message):
        k = self.permutation_key
        message = self._pad_message(message)
        return "".join([message[(i // len(k))*len(k) + k[i % len(k)] - 1] for i in range(len(message))])
    
    def _depermute_message(self, message):
        perm_key = np.array(self.permutation_key) - 1
        permutation = np.append(perm_key, [perm_key + len(self.permutation_key)*i for i in range(1, len(message) // len(self.permutation_key))])
        return "".join([message[np.where(permutation==i)[0][0]] for i in range(len(message))])
        
    def encrypt_message(self, raw_message):
        raw_message = self._permute_message(raw_message)
        return "".join([self.substitution_key[self.alphabet.index(raw_message[i].upper())] for i in range(len(raw_message))])
    
    def decrypt_message(self, encrypted_message):
        encrypted_message = self._depermute_message(encrypted_message)
        return "".join([self.alphabet[self.substitution_key.index(encrypted_message[i].upper())] for i in range(len(encrypted_message))])
```
The class above implements a couple of helper functions. `_pad_message` is used during the permutation step in case the number of characters in the message does not evenly divide the length of the permutation key. In this implementation, it will add the necessary number of "X"s at the end of the message.

`_permute_message` first applies padding to the raw imput, then using some clever modular arithmetic applies the permutation key. `_depermute_message` reverses the the permutation key. 

Finally, `encrypt_message` will call `_permute_message` and then apply Caesar Substitution on it and `decrypt message` will reverse both the permutation and substitution keys.

```py
perm = CaesarPermutationCipher("EFGHIJKLMNOPQRSTUVWXYZABCD", "32541")

encrypted = perm.encrypt_message("HELLOBEAUTIFULPERSON")
print(encrypted)
# 'PISPLEIXYFYJTPMWVRSI'

decrypted = perm.decrypt_message(encrypted)
print(decrypted)
# 'HELLOBEAUTIFULPERSON'
```
## 3. Vigenere cipher
The class below implements the algebraic method of implementing the *Viginere Cipher*: $C_i = (M_i + K_i)\ mod\ 26$ for encryption and $M_i = (C_i - K_i)\ mod\ 26$ for decryption. 

```py
class VigneteCipher():
    def __init__(self, keyword):
        self.keyword = keyword
        self.alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
    def encrypt_message(self, message):
        keyword = (self.keyword * (len(message) // len(self.keyword) + 1))[0:len(message)]
        encoded_as_nums = [(self.alphabet.index(message[i]) + self.alphabet.index(keyword[i])) % 26 for i in range(len(message))]
        return "".join([self.alphabet[i] for i in encoded_as_nums])
    
    def decrypt_message(self, message):
        keyword = (self.keyword * (len(message) // len(self.keyword) + 1))[0:len(message)]
        encoded_as_nums = [(self.alphabet.index(message[i]) - self.alphabet.index(keyword[i])) % 26 for i in range(len(message))]
        return "".join([self.alphabet[i] for i in encoded_as_nums])
```

## 4. Playfair cipher
The Cipher was implemented with the `PlayfairCipher` class which was too large to be included in its entirety here. First of all, when it is first instantiated it calls the `create_table` function, which constructs the 5x5 table containing the keyword. The core of the class is the `encrypt_message` method which goes through the following pipeline:
- applies some preprocessing to the initial message (adds an "X" between repeating letters in a digraph and pads the message at the end if necessary);
- it checks wether the two letters are in the same row or column and applies the corresponding rules if requires;
- if none of the above are true it applies the third rule.

The `decrypt_message` goes through a very similar pipeline but with some slight modifications.

```py
def encrypt_message(self, message):
    encrypted_message = ""
    message = self.preprocess(message)
    message = [message[i:i+2] for i in range(0, len(message), 2)]
    for pair in message:
        if pair[0] == "J":
            pair[0] = "I"
        if pair[1] == "J":
            pair[1] == "I"
            
        a = [int(item) for item in np.where(self.table == pair[0])] # coords of first letter
        b = [int(item) for item in np.where(self.table == pair[1])] # coords of second letter in pair
        
        is_same_col = self.same_col(pair[0], pair[1], a, b)
        is_same_row = self.same_row(pair[0], pair[1], a, b)
        if is_same_col:
            encrypted_message += self.table[(a[0] + 1) % 5, a[1]] + self.table[(b[0] + 1) % 5, b[1]]
        elif is_same_row:
            encrypted_message += self.table[a[0], (a[1] + 1) % 5] + self.table[b[0], (b[1] + 1) % 5]
        else:
            encrypted_message += self.table[a[0], b[1]] + self.table[b[0], a[1]]
    return encrypted_message
```

## Conclusions / Screenshots / Results
During this laboratory work I learned some new encryption algorithms and refreshed my knowledge of some I already know about. These algorithms of encryption belong to classical ciphers. Although it was fun to implement them, it can be concluded that these algorithms are not reliable and can be broken by whoever manages to find the key or even simplier in case of Caesar - the shift.
