from math import pi, sqrt, cos


def fidelity_2D(estimated_angle, true_angle):  # 3.1 Two dimensional coordinate systems
    return 0.5 + cos(true_angle-estimated_angle)*0.5

def average_fidelity_2D(N):  # eq 23
    return 0.5 + 0.25*N/(N+2)+1/(pi*(N+1))*sum([sqrt(1-((2*Nd-N)/(N+2))**2) for Nd in range(N+1)])


print(average_fidelity_2D(5))