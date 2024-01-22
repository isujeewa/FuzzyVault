import tkinter as tk
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from message import Message

def create_banner(width, height, text):
    # Create a Tkinter window
    root = tk.Tk()
    root.geometry(f"{width}x{height}")

    # Create a canvas to draw on
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    # Define font and brush for the text
    font = ("Arial", 24, "bold")
    brush = 'black'

    # Center the text on the canvas
    text_id = canvas.create_text(width // 2, height // 2, text=text, font=font, fill=brush)

    # Draw the current UTC time on the second line
    font = ("Arial", 12)
    current_time = datetime.now()
    second_line_text = current_time.strftime("%Y-%m-%d %H:%M:%S")
    second_line_id = canvas.create_text(width // 2, height // 2 + 20, text=second_line_text, font=font, fill=brush)

    # Run the Tkinter main loop
    root.update_idletasks()
    root.update()

    # Save the canvas as an image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((width // 2, height // 2), text, font=ImageFont.truetype("arial.ttf", 24), fill='black')
    draw.text((width // 2, height // 2 + 30), second_line_text, font=ImageFont.truetype("arial.ttf", 12), fill='black')
    return  image

# combine two images into one and have a option to split them back with the same bit pattern


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

    return combined_image

def split_images(combined_image):
    # Get metadata to determine the heights of individual images
    height1 = combined_image.info.get('height1', 0)
    height2 = combined_image.info.get('height2', 0)

    combined_image.info.pop('height1', None)
    combined_image.info.pop('height2', None)
   
    # Create two rectangles to represent the areas of the original images in the combined image
    rect1 = (0, 0, combined_image.width, height1)
    rect2 = (0, height1, combined_image.width, height2+height1)

    # Create two images to hold the split images
    split_image1 = combined_image.crop(rect1)
    split_image2 = combined_image.crop(rect2)


    return split_image1, split_image2


