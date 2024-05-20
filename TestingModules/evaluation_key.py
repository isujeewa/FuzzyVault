import numpy as np
from scipy.stats import chi2_contingency, chisquare
import string

def hex_to_binary(hex_key):
    return bin(int(hex_key, 16))[2:].zfill(len(hex_key) * 4)

def frequency_test(binary_key):
    ones = binary_key.count('1')
    zeroes = binary_key.count('0')
    n = len(binary_key)
    s_obs = ((ones - zeroes) ** 2) / n
    p_value = np.exp(-2 * s_obs)
    return s_obs, p_value

def serial_test(binary_key):
    n = len(binary_key)
    expected = n / 4
    patterns = ['00', '01', '10', '11']
    counts = {pattern: binary_key.count(pattern) for pattern in patterns}
    chi_square_stat = sum([(counts[pattern] - expected) ** 2 / expected for pattern in patterns])
    p_value = 1 - chi2_contingency([list(counts.values())])[1]
    return chi_square_stat, p_value

def chi_square_test(hex_key):
    expected = len(hex_key) / 16
    counts = {char: hex_key.count(char) for char in string.hexdigits[:16]}
    observed_values = list(counts.values())
    expected_values = [expected] * 16
    chi_square_stat, p_value = chisquare(f_obs=observed_values, f_exp=expected_values)
    return chi_square_stat, p_value

# Given key
key = "24f70b49dff18233edeb8960cd75ae1574704164758099e2c0f6e83459cf98b9"

# Convert to binary
binary_key = hex_to_binary(key)

# Perform tests
freq_stat, freq_p_value = frequency_test(binary_key)
serial_stat, serial_p_value = serial_test(binary_key)
chi_square_stat, chi_square_p_value = chi_square_test(key)

print(f"Frequency Test: Statistic={freq_stat}, p-value={freq_p_value}")
print(f"Serial Test: Statistic={serial_stat}, p-value={serial_p_value}")
print(f"Chi-Square Test: Statistic={chi_square_stat}, p-value={chi_square_p_value}")

if freq_p_value > 0.05:
    print("Frequency Test: The binary sequence appears random (p > 0.05).")
else:
    print("Frequency Test: The binary sequence does not appear random (p <= 0.05).")

if serial_p_value > 0.05:
    print("Serial Test: The binary sequence appears random (p > 0.05).")
else:
    print("Serial Test: The binary sequence does not appear random (p <= 0.05).")

if chi_square_p_value > 0.05:
    print("Chi-Square Test: The hexadecimal key appears random (p > 0.05).")
else:
    print("Chi-Square Test: The hexadecimal key does not appear random (p <= 0.05).")
