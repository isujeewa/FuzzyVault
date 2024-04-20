from PIL import Image
import numpy as np
from base64 import urlsafe_b64encode
from hashlib import sha256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from custom_exceptions import *

def generate_key(password):
    """Generates a secure encryption key from a given password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'some_salt',  # Should be securely saved & unique per user
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_decrypt(data, password, mode='enc'):
    """Encrypt or decrypt data using Fernet symmetric encryption."""
    key = generate_key(password)
    cipher = Fernet(key)
    return cipher.encrypt(data.encode()).decode() if mode == 'enc' else cipher.decrypt(data.encode()).decode()

def str_to_bin(data):
    """Convert string to binary."""
    return ''.join(format(ord(char), '08b') for char in data)

def bin_to_str(binary_data):
    """Convert binary string to text."""
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def modify_pixel(pixel, value):
    """Modifies the pixel's LSB based on the binary value provided."""
    if value == '0':
        return pixel & ~1
    else:
        return pixel | 1

def encode(image, text, password=None):
    """Encodes text into an image, with optional encryption."""
    if password:
        text = encrypt_decrypt(text, password, 'enc')
    binary_data = str_to_bin(text)
    data_length = format(len(binary_data), '032b')  # binary length of the data
    img = np.array(image)
    if len(data_length + binary_data) > img.size:
        raise DataError("The data size is too big to fit in this image!")

    flat_img = img.flatten()
    for i, bit in enumerate(data_length + binary_data):
        flat_img[i] = modify_pixel(flat_img[i], bit)
    img = flat_img.reshape(img.shape)
    return Image.fromarray(img)

def decode(image, password=None):
    """Decodes text from an image, with optional decryption."""
    img = np.array(image)
    flat_img = img.flatten()
    bits = ''.join(str(pixel & 1) for pixel in flat_img)
    length = int(bits[:32], 2)
    data = bin_to_str(bits[32:32 + length])
    if password:
        data = encrypt_decrypt(data, password, 'dec')
    return data

if __name__ == "__main__":
    choice = input('What do you want to do?\n1. Encrypt\n2. Decrypt\nInput(1/2): ')
    if choice == '1':
        input_file_path = input('Enter cover image path (with extension): ')
        secret_data = input('Enter secret data: ')
        password = input('Enter password (optional): ')
        output_file_path = input('Enter output image name (path) (with extension): ')
        try:
            input_image = Image.open(input_file_path)  # Load image from path
            output_image = encode(input_image, secret_data, password)
            output_image.save(output_file_path)  # Save the modified image
            print(f'Encoded successfully into {output_file_path}')
        except Exception as e:
            print(f"Error: {str(e)}")
    elif choice == '2':
        input_file_path = input('Enter stego image path: ')
        password = input('Enter password (optional): ')
        try:
            stego_image = Image.open(input_file_path)  # Load image from path
            extracted_data = decode(stego_image, password)
            print('Decrypted data:', extracted_data)
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print('Invalid choice.')