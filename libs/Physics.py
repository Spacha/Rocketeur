import math

def density(alt):
    if alt < 17500:
        return 1.213551 - 0.0001071568*alt + 2.612369e-9*alt**2
    elif alt < 27500:
        return 0.6857797 - 0.00004565179*alt + 7.903353e-10*alt**2
    elif alt < 40000:
        return 0.01
    elif alt < 70000:
        return 0.00007
    else:
        return 0


def gravity(alt):
    a = 0.0053024*math.sin(alt)
    b = 0.0000058*math.sin(2*alt)
    return 9.88*(1 + a*a - b*b)