import json
import numpy as np
from RSAKeyPair import ExtendedKeyPairGenerator
import base64
from io import BytesIO
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from message import Message
from steganography import hide_message, retrieve_message
from imageGen import create_banner,combine_images,split_images
from encryption import encrypt_image, decrypt_image
from fuzzy import capture_image_and_encoding, fuzzify_features, verify_user_and_get_password
from dataService import insert_profile_data, get_profile_data_by_email,get_all_profiles
from PIL import Image 
from common import encode_object, decode_object
import matplotlib.pyplot as plt
import keyGeneration 
import uuid
from fuzzyVault import FuzzyVault
from facialFeatureExtractor import FacialFeatureExtractor

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def decode_image_from_base64(base64_string):
    image_data = base64.b64decode(base64_string.split(",")[1])
    return cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('registration_com')
def handle_video_and_task(data):
    global values, user_actions, isResult
    video_frame = data.get('videoFrame')
    name = data.get('name')
    email = data.get('email')
    
    if video_frame is None:
        print("Error: 'videoFrame' not found in data dictionary.")
        return

    # Use regular expression to extract base64 text
    base64_text = re.search(r"data:image/jpeg;base64,(.*)", video_frame).group(1)
    image_data = base64.b64decode(base64_text)
    
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(BytesIO(image_data))

    facialFeatureExtractor = FacialFeatureExtractor()
    facialFeatures =  facialFeatureExtractor.capture_image_and_encoding("Registering your face. Press 'Enter' when ready...", image)
    if(facialFeatures is None):
        print("Unable to detect a face. Please align your face with the camera.")
        socketio.emit('result', {'status': 'false'})
        return
    else:
        
        fuzzy_vault = FuzzyVault()
        fuzzy_vault.register_user(facialFeatures)
        strend=encode_object(fuzzy_vault)

        #get new guid
         # Generate a UUID
        new_uuid = uuid.uuid4()
        # Convert the UUID to a string
        new_uuid_str = str(new_uuid)
        msg=insert_profile_data(new_uuid_str,name, email, strend)
        socketio.emit('result', {'status': 'true','msg':msg})
        # Show the image
        image.show()

@socketio.on('login_com')
def handle_video_and_task(data):
    global values, user_actions, isResult
    video_frame = data.get('videoFrame')
    email = data.get('email')
    print("email:", email)
    # Use regular expression to extract base64 text
    base64_text = re.search(r"data:image/jpeg;base64,(.*)", video_frame).group(1)
    image_data = base64.b64decode(base64_text)
    profile_data=get_profile_data_by_email(email)
    encodedVault =profile_data[3]
    vault=decode_object(encodedVault)
     # Open the image using PIL (Python Imaging Library)
    image2 = Image.open(BytesIO(image_data))

    facialFeatureExtractor = FacialFeatureExtractor()
    facialFeatures =  facialFeatureExtractor.capture_image_and_encoding("Registering your face. Press 'Enter' when ready...", image2)
    loginResult=vault.verify_user_and_get_password(facialFeatures)
    print("loginResult:", loginResult)
    print("profile_data:", profile_data)
    if(loginResult is None):
        socketio.emit('result', {'status': 'false'})
        return
    socketio.emit('result', {'status': 'true','guid':profile_data[0], 'name':profile_data[1], 'email':profile_data[2]})
    
    if video_frame is None:
        print("Error: 'videoFrame' not found in data dictionary.")
        return
    

@socketio.on('user_list_com')
def handle_video_and_task(data):
    global values, user_actions, isResult
 
    users = get_all_profiles()
     
    if(users is None):
        socketio.emit('result', {'status': 'false'})
        return
    socketio.emit('result', {'status': 'true','users':users})

@socketio.on('send_message_com') 
def handle_video_and_task(data):
    global values, user_actions, isResult   
    senderId = data.get('senderID')
    receiverId = data.get('receiverID')
    message = data.get('message')
    time = data.get('time')
    chanel_sender = f"{senderId}_{receiverId}"
    chanel_receiver = f"{receiverId}_{senderId}"
    print("chanel_sender:", chanel_sender)
    print("chanel_receiver:", chanel_receiver)
    print("message:", message)
    socketio.emit( chanel_sender, {'status': 'true', 'message':message, 'time':time ,'senderID':senderId, 'receiverID':receiverId})
    socketio.emit( chanel_receiver, {'status': 'true', 'message':message, 'time':time,'senderID':senderId, 'receiverID':receiverId})

   

    

if __name__ == '__main__':
    socketio.run(app, debug=True)
    #log
    print("Server started")




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




# Create a message object and serialize it to JSON
msgobj = Message()
msgobj.secret = "fuzzy_vault.get_key()"
msgorg = json.dumps(msgobj.__dict__)

print("password_string:", msgobj.secret )

#wait until user press enter
input("\nPress Enter to encrypt the image...")

imageName = "vegi.png"

# Create a banner image with the message
mainImage = Image.open(imageName)
height = 200
width =  mainImage.width
text = msgorg
# create the banner image print on the screen as log
print("Creating banner image with the message: ", text)

banner_img=create_banner(width, height, imageName)
banner_img.save("02_banner.jpg")
#banner image created and saved as banner.png
print("banner image created and saved as banner")
print("encording the message to the banner image and saving as encoded")
# banner image and encode the message
encoded_img = hide_message(banner_img, msgorg)
 
print("encording completed and saved as encoded.png")
print("decoding the message from the encoded image")

# encrypt the image
encrypted_img = encrypt_image(mainImage, msgobj.secret)

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



def view_base64_image(base64_string):
    # Decode the Base64 string
    image_data = base64.b64decode(base64_string)
    
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(BytesIO(image_data))
    
    # Show the image
    image.show()
 





