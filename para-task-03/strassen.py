#!/usr/bin/env python3

import sys
import numpy as np


def input_np_array(n):
    # n rounded up to the nearest power of 2
    n_rounded = 1 << (n - 1).bit_length()
    a = np.zeros((n_rounded, n_rounded), dtype=int)
    a[:n, :n] = np.array([[int(i) for i in input().split()] for _ in range(n)])
    return a


def split_np_array(a):
    m = len(a) / 2
    return a[:m, :m], a[:m, m:], a[m:, :m], a[m:, m:]


def strassen(a, b):
    n = len(a)
    if n == 1:
        return np.dot(a, b)
    c = np.ones((n, n), dtype=int)
    a11, a12, a21, a22 = split_np_array(a)
    b11, b12, b21, b22 = split_np_array(b)
    c11, c12, c21, c22 = split_np_array(c)

    p = []
    for i in range(7):
        p.append(np.empty((n, n), dtype=int))

    p[0] = strassen(a11 + a22, b11 + b22)
    p[1] = strassen(a21 + a22, b11)
    p[2] = strassen(a11, b12 - b22)
    p[3] = strassen(a22, b21 - b11)
    p[4] = strassen(a11 + a12, b22)
    p[5] = strassen(a21 - a11, b11 + b12)
    p[6] = strassen(a12 - a22, b21 + b22)

    c11 = p[0] + p[3] - p[4] + p[6]
    c12 = p[2] + p[4]
    c21 = p[1] + p[3]
    c22 = p[0] - p[1] + p[2] + p[5]

    m = n / 2
    c[:m, :m] = c11
    c[:m, m:] = c12
    c[m:, :m] = c21
    c[m:, m:] = c22

    return c


def main():
    if len(sys.argv) != 1:
        print('Usage: ./strassen.py')
        sys.exit(1)

    n = int(input())
    n_rounded = 1 << (n - 1).bit_length()
    a = input_np_array(n)
    b = input_np_array(n)

    c = strassen(a, b)

    for row in c[:n, :n]:
        for cell in row:
            print(cell, end=' ')
        print()

if __name__ == '__main__':
    main()
