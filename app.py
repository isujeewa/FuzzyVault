
import json
from message import Message
from steganography import hide_message, retrieve_message
from imageGen import create_banner,combine_images,split_images
from PIL import Image 



# Create a message object and serialize it to JSON
msgobj = Message()
msgorg = json.dumps(msgobj.__dict__)

# Create a banner image with the message
mainImage = Image.open("org_img.jpg")
height = 200
width =  mainImage.width
text = msgorg
# create the banner image print on the screen as log
print("Creating banner image with the message: ", text)

banner_img=create_banner(width, height, "Hello World")
banner_img.save("banner.jpg")
#banner image created and saved as banner.png
print("banner image created and saved as banner.png")
print("encording the message to the banner image and saving as encoded.png")
# banner image and encode the message
encoded_img = hide_message(banner_img, msgorg)
encoded_img.save("encoded.jpg")
print("encording completed and saved as encoded.png")
print("decoding the message from the encoded image")

# combine two images into one and have a option to split them back with the same bit pattern
#read image from the disk

combined_img= combine_images(encoded_img, mainImage)
combined_img.save("combined img.jpg")

#split images
img1,img2=split_images(combined_img )
img1.save("banner-recovered.jpg")
img2.save("org-recovered.jpg")

print("message decording")

# Decode the message from the encoded image
decoded_msg = retrieve_message(img1)

#log the decoded message
print(decoded_msg)
print("message decoding completed")






# Print or use the serialized string as needed
print(msgorg)
