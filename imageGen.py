import tkinter as tk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from message import Message
import numpy as np
import base64

from tkinter import Tk, Canvas
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

from tkinter import Tk, Canvas
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def calculate_text_width(text, font_size):
    #get char letngth
    char_length = len(text)
    #get char width
    char_width = 10
    tlenth = char_length * char_width
    if tlenth < 200:
        return 200

    return tlenth

def create_banner(width, height, text, message):
    # Truncate message if its length exceeds 100 characters
    message = message[:100]

    # Create a Tkinter window
    root = Tk()
    root.geometry(f"{width}x{height}")

    # Create a canvas to draw on
    canvas = Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    # Define font and brush for the text
    font = ("Arial", 24, "bold")
    brush = 'black'

    # Left align the text on the canvas
    text_id = canvas.create_text(20, height // 2, anchor='w', text=text, font=font, fill=brush)

    # Draw the current UTC time on the second line
    font = ("Arial", 12)
    current_time = datetime.now()
    second_line_text = current_time.strftime("%Y-%m-%d %H:%M:%S")
    second_line_id = canvas.create_text(20, height // 2 + 30, anchor='w', text=second_line_text, font=font, fill=brush)

    # Draw the message on the third line
    third_line_text = message
    third_line_id = canvas.create_text(20, height // 2 + 60, anchor='w', text=third_line_text, font=font, fill=brush)

    # Run the Tkinter main loop
    root.update_idletasks()
    root.update()

    # Save the canvas as an image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((20, height // 2), text, font=ImageFont.truetype("arial.ttf", 24), fill='black')
    draw.text((20, height // 2 + 30), second_line_text, font=ImageFont.truetype("arial.ttf", 12), fill='black')
    draw.text((20, height // 2 + 60), third_line_text, font=ImageFont.truetype("arial.ttf", 12), fill='black')
    
    return image


# combine two images into one and have a option to split them back with the same bit pattern
def create_image(width, height, message):
    # Truncate message if its length exceeds 100 characters
    message = message[:100]

    # Create a new PIL image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Define font and brush for the text
    secondary_text_font = ImageFont.truetype("arial.ttf", 12)
    brush = 'black'

    # Draw the current UTC time on the first line
    current_time = datetime.now()
    first_line_text = current_time.strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, height // 2), first_line_text, font=secondary_text_font, fill=brush)

    # Draw the message on the second line
    draw.text((20, height // 2 + 30), message, font=secondary_text_font, fill=brush)

    return image


def combine_images(image1, image2):
    # Determine the width and height for the combined image
    combined_width = image2.width;
    combined_height = image1.height + image2.height

    # Create a new image for the combined image
    combined_image = Image.new(image1.mode, (combined_width, combined_height), (255, 255, 255))

    # Paste the first image at the top
    combined_image.paste(image1, (0, 0))

    # Paste the second image at the bottom
    combined_image.paste(image2, (0, image1.height))

    # Save the combined image
    combined_image.save('combined_image.png')

    # Add metadata to store heights of individual images
    combined_image.info['height1'] = image1.height
    combined_image.info['height2'] = image2.height
    combined_image.save('combined_image.png')

    print("--------------------------")
    print(image1.height, image2.height)

    return combined_image

def split_images(combined_image):
    # Get metadata to determine the heights of individual images
    height1 = combined_image.info.get('height1', 0)
    height2 = combined_image.info.get('height2', 0)
    print("--------------------------")
    print(height1, height2)

    combined_image.info.pop('height1', None)
    combined_image.info.pop('height2', None)
   
    # Create two rectangles to represent the areas of the original images in the combined image
    rect1 = (0, 0, combined_image.width, height1)
    rect2 = (0, height1, combined_image.width, height2+height1)

    # Create two images to hold the split images
    split_image1 = combined_image.crop(rect1)
    split_image2 = combined_image.crop(rect2)


    return split_image1, split_image2

def split_images(combined_image ,height1, height2):
    # Get metadata to determine the heights of individual images
    print("--------------------------")
    print(height1, height2)

    # Create two rectangles to represent the areas of the original images in the combined image
    rect1 = (0, 0, combined_image.width, height1)
    rect2 = (0, height1, combined_image.width, height2+height1)

    # Create two images to hold the split images
    split_image1 = combined_image.crop(rect1)
    split_image2 = combined_image.crop(rect2)


    return split_image1, split_image2

def Get_Top_image(combined_image ,height1):
    # Get metadata to determine the heights of individual images
    print("--------------------------")
    print(height1)

    # Create two rectangles to represent the areas of the original images in the combined image
    rect1 = (0, 0, combined_image.width, height1)
    

    # Create two images to hold the split images
    split_image1 = combined_image.crop(rect1)
  


    return split_image1 


def encode_ndarray(arr):
    """
    Encode an NDArray to Base64.

    Parameters:
    arr (numpy.ndarray): The NDArray to encode.

    Returns:
    str: Base64 encoded string.
    """
    arr_bytes = arr.tobytes()
    encoded_data = base64.b64encode(arr_bytes)
    return encoded_data.decode('utf-8')

def decode_ndarray(encoded_data):
    """
    Decode a Base64 encoded string to NDArray.

    Parameters:
    encoded_data (str): Base64 encoded string.

    Returns:
    numpy.ndarray: Decoded NDArray.
    """
    decoded_bytes = base64.b64decode(encoded_data)
    arr = np.frombuffer(decoded_bytes, dtype=np.int32)
    return arr.reshape((-1, len(arr) // arr.shape[1]))


