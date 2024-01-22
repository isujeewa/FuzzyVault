
import json
import numpy as np
from message import Message
from steganography import hide_message, retrieve_message
from imageGen import create_banner,combine_images,split_images
from encryption import encrypt_image, decrypt_image
from fuzzy import capture_image_and_encoding, fuzzify_features, verify_user_and_get_password
from PIL import Image 
import matplotlib.pyplot as plt


  # Capture facial features
face_encoding = capture_image_and_encoding()

# Use "12345" as the password for fuzzification
stored_password = np.array([0, 4, 6, 8, 1,2])
# Convert the NumPy array to a list of strings
password_list = stored_password.astype(str).tolist()

# Convert the list to a plain string
password_string = "".join(password_list)

stored_encoding = face_encoding  # Store the initial facial encoding

# Fuzzify facial features
fuzzified_values = fuzzify_features(face_encoding)

print("Fuzzified Values:", fuzzified_values)


# Create a message object and serialize it to JSON
msgobj = Message()
msgobj.secret = password_string
msgorg = json.dumps(msgobj.__dict__)

print("password_string:", password_string)

# Create a banner image with the message
mainImage = Image.open("01_org_img.jpg")
height = 200
width =  mainImage.width
text = msgorg
# create the banner image print on the screen as log
print("Creating banner image with the message: ", text)

banner_img=create_banner(width, height, "Hello World")
banner_img.save("02_banner.jpg")
#banner image created and saved as banner.png
print("banner image created and saved as banner.png")
print("encording the message to the banner image and saving as encoded.png")
# banner image and encode the message
encoded_img = hide_message(banner_img, msgorg)
 
print("encording completed and saved as encoded.png")
print("decoding the message from the encoded image")

# encrypt the image
encrypted_img = encrypt_image(mainImage, password_string)

#save the encrypted image
encrypted_img.save("03_encrypted_img.jpg")


# combine two images into one and have a option to split them back with the same bit pattern
#read image from the disk

combined_img= combine_images(encoded_img, encrypted_img)
combined_img.save("04_combined img.jpg")
combined_img.show()
#split images
img1,img2=split_images(combined_img )


img1.save("05_banner-recovered.jpg")
img2.save("06_encrypted-recovered.jpg")

print("message decording")

# Decode the message from the encoded image
decoded_msg = retrieve_message(img1)

msgextracted= json.loads(decoded_msg)

msgobjRecovered = Message()
msgobjRecovered.__dict__ = msgextracted


 
# Assuming the necessary functions and variables are defined above
# ...

# Counter to limit the loop to 5 times
verification_attempts = 0

while verification_attempts < 5:
    # Allow the user to capture another snapshot for verification
    input("\nPress Enter to capture another snapshot for verification...")

    # Capture the second snapshot for verification
    verification_encoding = capture_image_and_encoding()

    # Verify the user and get the correct password
    correct_password = verify_user_and_get_password(verification_encoding, stored_encoding, stored_password)

    stored_password2 = np.array(correct_password)
    # Convert the NumPy array to a list of strings
    password_list = stored_password2.astype(str).tolist()

    # Convert the list to a plain string
    password_string = "".join(password_list)

    if correct_password is not None:
        if password_string == msgobjRecovered.secret:
            print("User Verified! Correct Password:", correct_password)

            # Decrypt the image
            decrypted_img = decrypt_image(img2, msgobjRecovered.secret)

            # Save and display the decrypted image
            decrypted_img.save(f"{verification_attempts + 1}_decrypted_img.jpg")
            decrypted_img.show()

            # Log the decoded message
            print(decoded_msg)
            print("Message decoding completed")

            # Increment the verification attempts counter
            verification_attempts =6

        else:
            print("User Verification Failed! Incorrect Password.")
            # Increment the verification attempts counter
            verification_attempts += 1

    else:
        print("User Verification Failed! Incorrect Password.")
         # Increment the verification attempts counter
        verification_attempts += 1

# End of the loop
print("Verification attempts limit reached.")




