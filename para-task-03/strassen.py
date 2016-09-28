#!/usr/bin/env python3

import sys
import numpy as np


def bin_ceil(n):
    """Round n up to the nearest power of 2."""
    return 1 << (n - 1).bit_length()


def split_mx_into_four(a):
    """Split a 2D numpy array into four equal arrays."""
    return [mx for submx in np.split(a, 2) for mx in np.hsplit(submx, 2)]


def strassen(a, b):
    """Multiply square matrices a and b using the Strassen algorithm."""
    if len(a) == 1:
        return np.dot(a, b)

    a11, a12, a21, a22 = split_mx_into_four(a)
    b11, b12, b21, b22 = split_mx_into_four(b)

    p1 = strassen(a11 + a22, b11 + b22)
    p2 = strassen(a21 + a22, b11)
    p3 = strassen(a11, b12 - b22)
    p4 = strassen(a22, b21 - b11)
    p5 = strassen(a11 + a12, b22)
    p6 = strassen(a21 - a11, b11 + b12)
    p7 = strassen(a12 - a22, b21 + b22)

    return np.hstack((np.vstack((p1 + p4 - p5 + p7, p3 + p5)),
                      np.vstack((p2 + p4, p1 - p2 + p3 + p6))))


def main():
    if len(sys.argv) != 1:
        print('Usage: ./strassen.py')
        sys.exit(1)

    n = int(input())
    n_rounded = bin_ceil(n)

    a = np.zeros((n_rounded, n_rounded), dtype=int)
    b = np.zeros((n_rounded, n_rounded), dtype=int)
    a[:n, :n], b[:n, :n] = np.vsplit(np.loadtxt(sys.stdin), 2)

    c = strassen(a, b)

    np.savetxt(sys.stdout.buffer, c[:n, :n], fmt='%d')


if __name__ == '__main__':
    main()
