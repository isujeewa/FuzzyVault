from PIL import Image

def hide_message(original_image, message):
    stego_image = original_image.copy()

    message_length = len(message)

    # Embed the message length in the first few pixels
    stego_image.putpixel((0, 0), (message_length, *stego_image.getpixel((0, 0))[1:]))

    pixel_index = 1

    # Embed each character of the message in the least significant bits of the pixel values
    for char in message:
        ascii_value = ord(char)

        # Embed each bit of the ASCII value in the least significant bit of the pixel value
        for bit_index in range(8):
            pixel = stego_image.getpixel((pixel_index % stego_image.width, pixel_index // stego_image.width))

            # Clear the least significant bit
            new_r = pixel[0] & 0xFE
            new_g = pixel[1] & 0xFE
            new_b = pixel[2] & 0xFE

            # Embed the current bit
            new_r |= (ascii_value >> bit_index) & 0x01
            new_g |= (ascii_value >> bit_index) & 0x01
            new_b |= (ascii_value >> bit_index) & 0x01

            # Update the pixel in the stego image
            stego_image.putpixel((pixel_index % stego_image.width, pixel_index // stego_image.width), (new_r, new_g, new_b))

            pixel_index += 1

    return stego_image

def retrieve_message(stego_image):
    pixel_index = 1

    # Retrieve the message length from the first few pixels
    message_length = stego_image.getpixel((0, 0))[0]

    message_chars = []

    # Retrieve each character of the message from the least significant bits of the pixel values
    for char_index in range(message_length):
        ascii_value = 0

        # Retrieve each bit of the ASCII value from the least significant bit of the pixel value
        for bit_index in range(8):
            pixel = stego_image.getpixel((pixel_index % stego_image.width, pixel_index // stego_image.width))

            # Extract the least significant bit
            lsb_r = pixel[0] & 0x01
            lsb_g = pixel[1] & 0x01
            lsb_b = pixel[2] & 0x01

            # Combine the bits to form the ASCII value
            ascii_value |= lsb_r << bit_index
            ascii_value |= lsb_g << bit_index
            ascii_value |= lsb_b << bit_index

            pixel_index += 1

        message_chars.append(chr(ascii_value))

    return ''.join(message_chars)

def hide_messagev2(original_image, message):
    stego_image = original_image.copy()

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Add a delimiter to mark the end of the message
    binary_message += '1111111111111110'

    pixel_index = 0
    width, height = original_image.size

    for y in range(height):
        for x in range(width):
            pixel = list(original_image.getpixel((x, y)))

            # Embed the message in the LSB of each color channel
            for i in range(3):
                if pixel_index < len(binary_message):
                    # Clear the least significant bit
                    pixel[i] &= 0xFE
                    # Embed the bit from the message
                    pixel[i] |= int(binary_message[pixel_index])
                    pixel_index += 1

            stego_image.putpixel((x, y), tuple(pixel))

            if pixel_index >= len(binary_message):
                return stego_image

    return stego_image

def extract_messagev2(stego_image):
    binary_message = ''
    width, height = stego_image.size

    for y in range(height):
        for x in range(width):
            pixel = stego_image.getpixel((x, y))

            # Extract the LSB from each color channel
            for i in range(3):
                binary_message += str(pixel[i] & 0x01)

    # Find the index of the delimiter marking the end of the message
    delimiter_index = binary_message.find('1111111111111110')

    # Extract the message bits and convert back to characters
    message_bits = binary_message[:delimiter_index]
    message = ''.join(chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8))

    return message



