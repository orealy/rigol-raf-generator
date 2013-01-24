#!/usr/bin/env python
"""
Simple program to generate a RAF file comprised of the sum of a set
of sinusoids.

The RAF file works for the DG4602.
"""
from math import pi
#from matplotlib import pylab as plt
import numpy as np

fileout = "gen.RAF"

def main():
    ffs = [40, 120] # Fundamental frequencies
    amps = [1, 1] # Amplitudes of those frequecies
    nsamps = 2**13

    gcd = get_gcd(ffs)
    x = np.r_[0:nsamps]
    sinusoids = np.array([np.sin(x * freq/gcd * 2*pi / nsamps) for freq in ffs])

    amps = np.array([amps], dtype=float)
    amps = amps/np.max(amps)

    print amps.shape
    total = np.sum(sinusoids*amps.T, 0)

    to_raf(total)

def to_raf(signal):
    """Convert the signal (already the correct length) to a RAF file."""

    # Shift and convert the signal
    signal = signal - signal.min()
    signal = ((signal/signal.max()) * int("3fff", 16)).astype('int16')

    # Write the signal as binary.
    fp = open(fileout, "w")
    signal.tofile(fp)

def get_gcd(nums):
    """Find the greates common divisor of a list"""
    def gcd(a,b):
        while b:
            a, b = b, a%b
        return a
    return reduce(gcd, nums)

if __name__ == "__main__":
    main()
