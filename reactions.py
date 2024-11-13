from mpmath import pi, exp
from constants import *

def K_of_H_ionization(T):
    return ((gp * ge )/ gH) * ((2 * pi * kB * T * me/ (h*h))**1.5) * exp(-dE1/(kB * T))

def K_of_H2_decomposition(T):
    # return ((gH * gH )/ gH2) * ((2 * pi * kB * T / (h*h))**1.5) *(((mH * mH)/mH2)**1.5)*exp(-dE2/(kB * T))
    return ((gH * gH )/ gH2) * ((2 * pi * kB * T / (h*h))**1.5) *(((mH * mH)/mH2)**1.5)*exp(-dE2/(kB * T)) / (T/T_H2_rotation)

def K_of_H_first_excitation(T):
    return (gH_first / gH) * exp( -(dE1 * (1 - 1/4)) / (kB * T))

def K_of_H_second_excitation(T):
    return (gH_second / gH) * exp( -(dE1 * (1 - 1/9)) / (kB * T))

def K_of_H_third_excitation(T):
    return (gH_third / gH) * exp( -(dE1 * (1 - 1/16)) / (kB * T))

def K_of_H2_primary_decomposition(T):
    return ((gH2_ion * ge )/ gH2) * ((2 * pi * kB * me*T / (h*h))**1.5) *exp(-dE3/(kB * T))

if __name__ == "__main__":
    print(dE2/kB)
    print(dE1/kB)
    print((dE3-dE1-dE2)/dE3)