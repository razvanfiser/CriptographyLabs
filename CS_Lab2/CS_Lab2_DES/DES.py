import numpy as np
import Tables as t

class DES():
    def __init__(self, K, PC_1, PC_2, IP, E_bit, S, P, IP_inverse):
        self.K = K
        self.PC_1 = PC_1
        self.PC_2 = PC_2
        self.IP = IP
        self.E_bit = E_bit
        self.S = [np.array(S_n) for S_n in S]
        self.P = P
        self.IP_inverse = IP_inverse

    def permute(self, a, b):
        res = [a[b[i] - 1] for i in range(len(b))]
        return "".join(res)

    def split(self, a):
        return "".join(a[0: int(len(a)/2)]), "".join(a[int(len(a)/2): ])

    def shift(self, a, n):
        return "".join(a[0+n:] + a[:n])

    def xor(self, a, b):
        res = [str((int(a[i]) + int(b[i])) % 2) for i in range(len(a))]
        return "".join(res)

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

    def encrypt(self, message):
        message_list = [message[i:i+64] for i in range(0, len(message), 64)]
        if len(message) % 64 != 0:
            # leftover = message[64*(len(message) // 64) :] + '0'*(64 - (len(message) % 64))
            # message_list.append(leftover)
            message_list[-1] += '0'*(64 - (len(message) % 64))
        return "".join(self.step_2(m) for m in message_list)

    def step_2_decrypt(self, message):
        K = self.obtain_subkeys()[::-1]
        M_IP = self.permute(message, self.IP)
        L_0, R_0 = self.split(M_IP)
        L, R = [L_0], [R_0]

        for i in range(16):
            L.append(R[i])
            R.append(self.xor(L[i], self.f(R[i], K[i])))
        R16L16 = R[16] + L[16]
        return self.permute(R16L16, self.IP_inverse)

    def decrypt(self, message):
        message_list = [message[i:i + 64] for i in range(0, len(message), 64)]
        return "".join(self.step_2_decrypt(m) for m in message_list)