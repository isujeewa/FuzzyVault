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


from PIL import Image

def hide_messagev2(original_image, message):
    stego_image = original_image.copy()

    message_length = len(message)

    # Embed the message length in the first few pixels
    message_length_bytes = message_length.to_bytes(4, 'big')  # Convert to 4-byte big-endian integer
    for i in range(4):
        stego_image.putpixel((0, i), (message_length_bytes[i], *stego_image.getpixel((0, i))[1:]))

    pixel_index = 4  # Start from the 5th pixel

    # Embed each character of the message in the pixel values
    for char in message:
        ascii_value = ord(char)

        # Embed each byte of the ASCII value in the pixel values
        for i in range(3):  # Embed in R, G, B components
            pixel = stego_image.getpixel((pixel_index % stego_image.width, pixel_index // stego_image.width))

            # Clear the least significant bit
            new_component = pixel[i] & 0xFE

            # Embed the current byte
            new_component |= (ascii_value >> (i * 8)) & 0x01

            # Update the pixel in the stego image
            new_pixel = list(pixel)
            new_pixel[i] = new_component
            stego_image.putpixel((pixel_index % stego_image.width, pixel_index // stego_image.width), tuple(new_pixel))

            pixel_index += 1

    return stego_image

def retrieve_messagev2(stego_image):
    pixel_index = 4  # Start from the 5th pixel

    # Retrieve the message length from the first few pixels
    message_length_bytes = [stego_image.getpixel((0, i))[0] for i in range(4)]
    message_length = int.from_bytes(message_length_bytes, 'big')

    message_chars = []

    # Retrieve each character of the message from the pixel values
    for _ in range(message_length):
        ascii_value = 0

        # Retrieve each byte of the ASCII value from the pixel values
        for i in range(3):  # Extract from R, G, B components
            pixel = stego_image.getpixel((pixel_index % stego_image.width, pixel_index // stego_image.width))

            # Extract the least significant bit
            lsb = pixel[i] & 0x01

            # Combine the bits to form the ASCII value
            ascii_value |= lsb << (i * 8)

            pixel_index += 1

        message_chars.append(chr(ascii_value))

    return ''.join(message_chars)


# Example usage:
# original_image = Image.open("example_image.png")
# stego_image = hide_message(original_image, "Your message here")
# stego_image.save("stego_image.png")
# retrieved_message = retrieve_message(stego_image)
# print("Retrieved message:", retrieved_message)


# Example usage:
# original_image = Image.open("path/to/your/image.png")
# hidden_message = "Your secret message"
# stego_image = hide_message(original_image, hidden_message)
# stego_image.show()
# retrieved_message = retrieve_message(stego_image)
# print(retrieved_message)
