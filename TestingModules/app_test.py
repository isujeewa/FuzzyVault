
import json
import numpy as np
from RSAKeyPair import ExtendedKeyPairGenerator

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from message import Message
from steganography import hide_message, retrieve_message
from imageGen import Get_Top_image, create_banner,combine_images,split_images
from encryption import encrypt_image, decrypt_image
from fuzzy import capture_image_and_encoding, fuzzify_features, verify_user_and_get_password
from PIL import Image 
import matplotlib.pyplot as plt
import keyGeneration

from fuzzyVault import FuzzyVault


key_pair_generator = ExtendedKeyPairGenerator()
key_pair_generator.save_key_pair()

# Example usage:
data_to_encrypt = "Sensitive information"

# Encrypt the data using the public key
encrypted_data = key_pair_generator.encrypt_data(data_to_encrypt, key_pair_generator.public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
))

print(f"Encrypted data: {encrypted_data}")

# Decrypt the data using the private key
decrypted_data = key_pair_generator.decrypt_data(encrypted_data)
print(f"Decrypted data: {decrypted_data}")


  # Capture facial features
face_encoding = capture_image_and_encoding("Registering your face. Press 'Enter' when ready...")

fuzzy_vault = FuzzyVault()
fuzzy_vault.register_user(face_encoding)


# Create a message object and serialize it to JSON
msgobj = Message()

msgobj.secret = fuzzy_vault.get_key()


print("password_string:", msgobj.secret )

#wait until user press enter
input("\nPress Enter to encrypt the image...")

file_path = "Testing"
file_path_2 = "TestingDetails"
file_name = "vegi"
file_type = "png"

imageName = f"{file_name}.{file_type}"
fileType=".png"
# Create a banner image with the message
mainImage = Image.open(imageName)
height = 200
width =  mainImage.width
file_name = "01_org_img"
path = "\\".join([file_path, f"{file_name}.{file_type}"])
path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])

mainImage.save(path)
mainImage.save(path2)

# encrypt the image
encrypted_img = encrypt_image(mainImage, msgobj.secret)

#save the encrypted image
file_name = "02_encrypted_img"
encrypted_img.save(path2)


msgobj.height2 = encrypted_img.height

banner_img=create_banner(width, height, imageName,"test message")
#save to testresult folde
file_name = "03_banner"
path = "\\".join([file_path, f"{file_name}.{file_type}"])
path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])
banner_img.save(path2)
msgobj.height1 = banner_img.height
msgorg = json.dumps(msgobj.__dict__)
text = msgorg
# create the banner image print on the screen as log
print("Creating banner image with the message: ", text)
#banner image created and saved as banner.png
print("banner image created and saved as banner")
print("encording the message to the banner image and saving as encoded")
# banner image and encode the message
encoded_img = hide_message(banner_img, msgorg)
 
print("encording completed and saved as encoded.png")
print("decoding the message from the encoded image")




# combine two images into one and have a option to split them back with the same bit pattern
#read image from the disk

combined_img= combine_images(encoded_img, encrypted_img)
file_name = "04_combined img"
path = "\\".join([file_path, f"{file_name}.{file_type}"])
path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])
combined_img.save(path)
combined_img.save(path2)
combined_img.show()

top_image_section = Get_Top_image(combined_img, 200)


decoded_msg = retrieve_message(top_image_section)
msgextracted= json.loads(decoded_msg)

print("height1:", msgextracted['height1'])
print("height2:", msgextracted['height2'])
#split images
img1,img2=split_images(combined_img ,msgextracted['height1'],msgextracted['height2'])

file_name = "05_banner-recovered"
path = "\\".join([file_path, f"{file_name}.{file_type}"])
path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])


img1.save(path2)
file_name = "06_encrypted-recovered"
path = "\\".join([file_path, f"{file_name}.{file_type}"])
path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])

img2.save(path2)

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
    verification_encoding = capture_image_and_encoding( "Capturing your face for verification. Press 'Enter' when ready...")

    # Verify the user and get the correct password
    correct_password =  fuzzy_vault.verify_user_and_get_password(verification_encoding)

    stored_password2 = np.array(correct_password)
    print("stored_password2:", stored_password2)

    # Convert the NumPy array to a list of strings
    password_list = stored_password2.astype(str).tolist()

    # Convert the list to a plain string
    password_string = "".join(password_list)

    if correct_password is not None and "-1":
        if password_string == msgobjRecovered.secret:
            print("User Verified! Correct Password:", correct_password)

            # Decrypt the image
            decrypted_img = decrypt_image(img2, msgobjRecovered.secret)

            file_name = "07decrypted_img"
            path = "\\".join([file_path, f"{file_name}.{file_type}"])
            path2 = "\\".join([file_path_2, f"{file_name}.{file_type}"])
            # Save and display the decrypted image
            decrypted_img.save(path)
            decrypted_img.save(path2)

         

            decrypted_img.show()

            # Log the decoded message
            print(decoded_msg)
            print("Message decoding completed")

            # Increment the verification attempts counter
            verification_attempts =6

        elif correct_password ==  "-1":
            print("Unable to detect a face. Please align your face with the camera.")
            # Increment the verification attempts counter
            verification_attempts += 1

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