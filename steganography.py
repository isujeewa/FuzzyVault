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

# Example usage:
# original_image = Image.open("path/to/your/image.png")
# hidden_message = "Your secret message"
# stego_image = hide_message(original_image, hidden_message)
# stego_image.show()
# retrieved_message = retrieve_message(stego_image)
# print(retrieved_message)
