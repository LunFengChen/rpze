import matplotlib.pyplot as plt

M = []
for i in range(0, 136):
    M.append(0)
for i in range(136, 151):
    M.append(1 / 15)

N = [0]
for i in range(1, 137):
    N.append(1 / 143)
for i in range(137, 151):
    N.append((151 - i) / 2145)


def J(A, B):
    if len(A) > len(B):
        C = A
        A = B
        B = C
    N = []
    for i in range(0, len(A) - 1):
        N.append(sum(A[j] * B[i - j] for j in range(0, i + 1)))
    for i in range(len(A) - 1, len(B)):
        N.append(sum(A[j] * B[i - j] for j in range(0, len(A))))
    for i in range(len(B), len(B) + len(A) - 1):
        N.append(sum(A[j] * B[i - j] for j in range(i - len(B) + 1, len(A))))
    return N


def S(a):
    if a == 0:
        T = []
        for i in range(0, 136):
            T.append(-i / 143 + 1)
        for i in range(136, 150):
            T.append((i - 150) * (i - 151) / 4290)
        return T
    elif a == 1:
        T = []
        for i in range(0, 136):
            T.append(i / 143)
        for i in range(136, 150):
            T.append(-(i - 136) * (i - 150) / 2145 + 136 / 143)
        for i in range(150, 272):
            T.append(-i / 143 + 2)
        for i in range(272, 286):
            T.append((i - 270) * (i - 271) * (i - 272) / 193050 - i / 143 + 2)
        for i in range(286, 300):
            T.append(-(i - 300) * (i - 301) * (i - 302) / 193050)
        return T
    else:
        return J(S(a - 1), M)


def R(a):
    T = M
    for i in range(0, a - 1):
        T = J(T, M)
    return T


Q = J(N, R(2))
plt.bar(list(range(0, len(Q))), Q)
plt.show()
