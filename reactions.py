from mpmath import pi, exp
from constants import *

def K_of_H_ionization(T):
    return ((gp * ge )/ gH) * ((2 * pi * kB * T / (h*h))**1.5) *(((mp * me)/mH)**1.5)*exp(-dE1/(kB * T))

def K_of_H2_decomposition(T):
    # return ((gH * gH )/ gH2) * ((2 * pi * kB * T / (h*h))**1.5) *(((mH * mH)/mH2)**1.5)*exp(-dE2/(kB * T))
    return ((gH * gH )/ gH2) * ((2 * pi * kB * T / (h*h))**1.5) *(((mH * mH)/mH2)**1.5)*exp(-dE2/(kB * T)) / (T/T_H2_rotation)

def K_of_H2_primary_decomposition(T):
    return ((gH2_ion * ge )/ gH2) * ((2 * pi * kB * me*T / (h*h))**1.5) *exp(-dE3/(kB * T))

def K_of_electron_pair(T):
    return (ge*ge) * ((2 * pi * kB * me*T / (h*h))**3) * exp(-(2 * me * c*c)/(kB * T))

if __name__ == "__main__":
    print(dE2/kB)
    print(dE1/kB)
    print((dE3-dE1-dE2)/dE3)