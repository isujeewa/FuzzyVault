from PIL import Image
import random

def encrypt_image(original_image, key):
    encrypted_image = Image.new('RGB', (original_image.width, original_image.height))

    # Get a list of all pixel positions
    pixel_positions = list(range(original_image.width * original_image.height))

    # Shuffle the pixel positions using Fisher-Yates algorithm
    random.seed(hash(key))
    random.shuffle(pixel_positions)

    # Iterate through the shuffled pixel positions
    for i in range(len(pixel_positions)):
        original_x = pixel_positions[i] % original_image.width
        original_y = pixel_positions[i] // original_image.width

        new_x = i % original_image.width
        new_y = i // original_image.width

        # Get the original pixel color
        original_color = original_image.getpixel((original_x, original_y))

        # Apply XOR operation to each color channel (RGB) with ASCII value of corresponding key character
        r = (original_color[0] ^ ord(key[i % len(key)])) % 256
        g = (original_color[1] ^ ord(key[i % len(key)])) % 256
        b = (original_color[2] ^ ord(key[i % len(key)])) % 256

        # Set the encrypted pixel color at the shuffled position
        encrypted_image.putpixel((new_x, new_y), (r, g, b))

    return encrypted_image

def decrypt_image(encrypted_image, key):
    decrypted_image = Image.new('RGB', (encrypted_image.width, encrypted_image.height))

    # Get a list of all pixel positions
    pixel_positions = list(range(encrypted_image.width * encrypted_image.height))

    # Shuffle the pixel positions using Fisher-Yates algorithm with the same key
    random.seed(hash(key))
    random.shuffle(pixel_positions)

    # Iterate through the shuffled pixel positions
    for i in range(len(pixel_positions)):
        original_x = pixel_positions[i] % encrypted_image.width
        original_y = pixel_positions[i] // encrypted_image.width

        new_x = i % encrypted_image.width
        new_y = i // encrypted_image.width

        # Get the encrypted pixel color
        encrypted_color = encrypted_image.getpixel((new_x, new_y))

        # Apply XOR operation to each color channel (RGB) with ASCII value of corresponding key character
        r = (encrypted_color[0] ^ ord(key[i % len(key)])) % 256
        g = (encrypted_color[1] ^ ord(key[i % len(key)])) % 256
        b = (encrypted_color[2] ^ ord(key[i % len(key)])) % 256

        # Set the decrypted pixel color at the shuffled position
        decrypted_image.putpixel((original_x, original_y), (r, g, b))

    return decrypted_image