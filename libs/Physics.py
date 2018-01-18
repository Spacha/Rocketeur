import math

def density(alt):
    return 1.213551 - 0.0001071568*alt + 2.612369e-9*alt**2

def gravity(alt):
    a = 0.0053024*math.sin(alt)
    b = 0.0000058*math.sin(2*alt)
    return 9.88*(1 + a*a - b*b)