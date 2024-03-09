from PIL import Image
import random

def encrypt_image(source_image, secret_key):
    encrypted_img = Image.new('RGB', (source_image.width, source_image.height))

    # Get a list of all pixel positions
    pixel_positions = list(range(source_image.width * source_image.height))

    # Shuffle the pixel positions using Fisher-Yates algorithm
    random.seed(hash(secret_key))
    random.shuffle(pixel_positions)

    # Iterate through the shuffled pixel positions
    for i in range(len(pixel_positions)):
        original_x = pixel_positions[i] % source_image.width
        original_y = pixel_positions[i] // source_image.width

        new_x = i % source_image.width
        new_y = i // source_image.width

        # Get the original pixel color
        original_color = source_image.getpixel((original_x, original_y))

        # Apply XOR operation to each color channel (RGB) with ASCII value of corresponding key character
        r = (original_color[0] ^ ord(secret_key[i % len(secret_key)])) % 256
        g = (original_color[1] ^ ord(secret_key[i % len(secret_key)])) % 256
        b = (original_color[2] ^ ord(secret_key[i % len(secret_key)])) % 256

        # Set the encrypted pixel color at the shuffled position
        encrypted_img.putpixel((new_x, new_y), (r, g, b))

    return encrypted_img

def decrypt_image(encrypted_img, secret_key):
    decrypted_img = Image.new('RGB', (encrypted_img.width, encrypted_img.height))

    # Get a list of all pixel positions
    pixel_positions = list(range(encrypted_img.width * encrypted_img.height))

    # Shuffle the pixel positions using Fisher-Yates algorithm with the same key
    random.seed(hash(secret_key))
    random.shuffle(pixel_positions)

    # Iterate through the shuffled pixel positions
    for i in range(len(pixel_positions)):
        original_x = pixel_positions[i] % encrypted_img.width
        original_y = pixel_positions[i] // encrypted_img.width

        new_x = i % encrypted_img.width
        new_y = i // encrypted_img.width

        # Get the encrypted pixel color
        encrypted_color = encrypted_img.getpixel((new_x, new_y))

        # Apply XOR operation to each color channel (RGB) with ASCII value of corresponding key character
        r = (encrypted_color[0] ^ ord(secret_key[i % len(secret_key)])) % 256
        g = (encrypted_color[1] ^ ord(secret_key[i % len(secret_key)])) % 256
        b = (encrypted_color[2] ^ ord(secret_key[i % len(secret_key)])) % 256

        # Set the decrypted pixel color at the shuffled position
        decrypted_img.putpixel((original_x, original_y), (r, g, b))

    return decrypted_img
