# Skrypt do optymalizacji logiki timera 3-bitowego
from sympy import symbols, SOPform

# Q2, Q1, Q0 - stan obecny
q = symbols('q2 q1 q0')

# Mintermy dla licznika w dół (7->6, 6->5, ..., 1->0, 0->0)
# N2, N1, N0 to stany następne
n2_minterms = [5, 6, 7] # Wartości Q dla których N2=1
n1_minterms = [3, 4, 7] # Wartości Q dla których N1=1
n0_minterms = [2, 4, 6] # Wartości Q dla których N0=1

print(f"Funkcja dla D2: {SOPform(q, n2_minterms)}")
print(f"Funkcja dla D1: {SOPform(q, n1_minterms)}")
print(f"Funkcja dla D0: {SOPform(q, n0_minterms)}")