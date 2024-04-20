from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import os
import numpy as np

def generate_random_password():
    # Generate a random password
    random_password = np.arange(20)
    np.random.shuffle(random_password)

    # Convert the password to a string
    random_password_str = ''.join(map(str, random_password))

    random_password_str = np.array([int(x) for x in random_password_str])

    return random_password_str

def generate_random_key():
    # Generate a random password
    random_password = np.arange(20)
    np.random.shuffle(random_password)

    # Convert the password to a string
    random_password_str = ''.join(map(str, random_password))

    return random_password_str

def get_ndarray_from_string(s):
    # Ensure the string consists of digits and convert each character to an integer
    if s.isdigit():  # Check if all characters in the string are digits
        int_array = np.array([int(char) for char in s], dtype=np.int32)
        return int_array
    else:
        raise ValueError("The string contains non-digit characters")

def get_string_from_array(int_array):
    # Assumes the array consists of integers that are originally single digits
    return ''.join(map(str, int_array))

def prepare_key(numeric_key):
    """Prepare a cryptographic key from a numeric string."""
    # Convert numeric key to bytes, hash it to generate a fixed-size (32 bytes) key
    hash_key = sha256(numeric_key.encode()).digest()
    return hash_key[:32]  # Ensure the key is 32 bytes, suitable for AES-256

def encrypt(data, key):
    """Encrypt data using AES encryption with CBC mode."""
    iv = os.urandom(16)  # AES block size for CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad data to be multiple of 16 bytes
    padded_data = data + b' ' * (16 - len(data) % 16)
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted  # Prepend IV for use in decryption

def decrypt(encrypted_data, key):
    """Decrypt data using AES encryption with CBC mode."""
    iv = encrypted_data[:16]  # Extract IV
    encrypted_data = encrypted_data[16:]  # Remove IV from data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.strip()

# testing the functions
numeric_key = "306819141215165111947101318172"
key = prepare_key(numeric_key)
random_password = get_string_from_array(generate_random_password())
data = random_password.encode('utf-8')  # Convert to bytes

encrypted_data = encrypt(data, key)
decrypted_data = decrypt(encrypted_data, key).decode('utf-8')  # Decode bytes to string

print("Original Data:", random_password)
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data)