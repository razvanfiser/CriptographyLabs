import Tables as t
import DES
import numpy as np

M = "0000000100100011010001010110011110001001101010111100110111101111"
K = "0001001100110100010101110111100110011011101111001101111111110001"

M2 = "".join([str(num) for num in list(np.random.randint(0, 2, 64))])
K2 = "".join([str(num) for num in list(np.random.randint(0, 2, 64))])

print("Example in PDF")
des = DES.DES(K, t.PC_1, t.PC_2, t.IP, t.E_bit, t.S, t.P, t.IP_inverse)
encrypted_message = des.encrypt(M)
print(encrypted_message)
decrypted_message = des.decrypt(encrypted_message)
print(decrypted_message)
print(M == decrypted_message)
print()

print("My example")
des = DES.DES(K2, t.PC_1, t.PC_2, t.IP, t.E_bit, t.S, t.P, t.IP_inverse)
encrypted_message = des.encrypt(M2)
print(encrypted_message)
decrypted_message = des.decrypt(encrypted_message)
print(decrypted_message)
print(M2 == decrypted_message)
