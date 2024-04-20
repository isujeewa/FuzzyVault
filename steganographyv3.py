from PIL import Image

def str_to_binary(message):
    """Convert a string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in message)

def binary_to_str(binary_message):
    """Convert a binary string to ASCII string."""
    return ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

def embed_data_in_image(image, data):
    """Embed binary data into an image's least significant bits."""
    binary_data = data + '1111111111111110'  # Delimiter to mark the end
    pixels = image.load()
    width, height = image.size

    pixel_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            for i in range(3):
                if pixel_index < len(binary_data):
                    bit = int(binary_data[pixel_index])
                    if i == 0:
                        r = (r & ~1) | bit
                    elif i == 1:
                        g = (g & ~1) | bit
                    elif i == 2:
                        b = (b & ~1) | bit
                    pixel_index += 1
                pixels[x, y] = (r, g, b)
                if pixel_index >= len(binary_data):
                    return image
    return image

def extract_data_from_image(image):
    """Extract binary data from an image's least significant bits."""
    pixels = image.load()
    width, height = image.size
    binary_data = ''

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += f'{r & 1}{g & 1}{b & 1}'

    delimiter = '1111111111111110'
    delimiter_index = binary_data.find(delimiter)
    if delimiter_index != -1:
        return binary_to_str(binary_data[:delimiter_index])
    return None

def hide_message(image_path, message, output_path):
    """Hide a message within an image."""
    image = Image.open(image_path)
    binary_message = str_to_binary(message)
    stego_image = embed_data_in_image(image.copy(), binary_message)
    stego_image.save(output_path)

def retrieve_message(image_path):
    """Retrieve a hidden message from an image."""
    image = Image.open(image_path)
    message = extract_data_from_image(image)
    return message

# Example usage
if __name__ == "__main__":
    input_image_path = "vegi.png"
    output_image_path = "vegi_v3.png"
    message = "Hello, this is a hidden message!"

    hide_message(input_image_path, message, output_image_path)
    extracted_message = retrieve_message(output_image_path)
    print("Extracted message:", extracted_message)
