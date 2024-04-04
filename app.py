import io
import json
import os
import numpy as np
from RSAKeyPair import ExtendedKeyPairGenerator
import base64
from io import BytesIO
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from message import Message
from steganography import hide_message, retrieve_message
from imageGen import Get_Top_image, create_banner,combine_images,split_images
from encryption import encrypt_image, decrypt_image
from fuzzy import capture_image_and_encoding, fuzzify_features, verify_user_and_get_password
from dataService import insert_profile_data, get_profile_data_by_email,get_all_profiles,get_profile_data_by_guid
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
socketio = SocketIO(app, cors_allowed_origins='*',max_http_buffer_size=1e7)

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
    print("image2:", image2)

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

@socketio.on('keyExchange') 
def handle_video_and_task(data):
    global values, user_actions, isResult
    senderId = data.get('senderID')
    receiverId = data.get('receiverID')
    profile_data_sender=get_profile_data_by_guid(senderId)
    encodedVault_sender =profile_data_sender[3]
    vault_sender=decode_object(encodedVault_sender)   
    key_sender = vault_sender.get_key()
    profile_data_receiver=get_profile_data_by_guid(receiverId)
    encodedVault_receiver =profile_data_receiver[3]
    vault_receiver=decode_object(encodedVault_receiver)   
    key_receiver = vault_receiver.get_key()
    print("key_sender:", key_sender)
    print("key_receiver:", key_receiver)
      

@socketio.on('send_message_com') 
def handle_video_and_task(data):
    global values, user_actions, isResult   
    senderId = data.get('senderID')
    receiverId = data.get('receiverID')
    message = data.get('message')
    encryptionOption = data.get('encryptionOption')
    fileName = data.get('fileName')
    type = data.get('type')
    time = data.get('time')
    chanel_sender = f"{senderId}_{receiverId}"
    chanel_receiver = f"{receiverId}_{senderId}"
    print("chanel_sender:", chanel_sender)
    print("chanel_receiver:", chanel_receiver)

    print("type:", type)
    #base64_text = re.search(r"data:image/png;base64,(.*)", file).group(1)
    #split by coma
    if type =='0':
        socketio.emit( chanel_sender, {'status': 'true', 'message':message, 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':''})
        socketio.emit( chanel_receiver, {'status': 'true', 'message':message, 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':''})
    if type =='1':
        #cooment image received
        print("image received")
        image_data_base64_bysender = data['file'].split(',')[1]  # remove the 'data:image/png;base64,' prefix
        image_data_base64_bysender_type = data['file'].split(',')[0].split(';')[0].split('/')[-1]
        image_data_bytes_bysender = base64.b64decode(image_data_base64_bysender)
        image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
        print("processed the image")
        profile_data_receiver=get_profile_data_by_guid(receiverId)
        encodedVault_receiver =profile_data_receiver[3]
        vault_receiver=decode_object(encodedVault_receiver)   
        key_receiver = vault_receiver.get_key()
        print("vault created")

        height = 200
        width =  image_bysender.width
        banner_img=create_banner(width, height, fileName)
        print(image_bysender.filename)
        print("banner_img created")
        # Create a message object and serialize it to JSON
        encrypted_img = encrypt_image(image_bysender, key_receiver)
        print("encrypted_img created")
        msgobj = Message()
        #msgobj.secret = key_receiver
        #last 4 digit of the key_receiver
        msgobj.secret = key_receiver[-4:]
        msgobj.height1 = banner_img.height
        msgobj.height2 = encrypted_img.height
        msgorg = json.dumps(msgobj.__dict__)
       
        print("message created ")
        encoded_img = hide_message(banner_img, msgorg)
        print("added message to image")
        
        combined_img= combine_images(encoded_img, encrypted_img)
         
        print("combined image created")
 
        print("file_type:", image_data_base64_bysender_type)
        # Convert the image to bytes and then encode to base64
        combined_img_byte_array = io.BytesIO()
        combined_img.save(combined_img_byte_array, format=image_data_base64_bysender_type)
        encoded_img_bytes = combined_img_byte_array.getvalue()
        combined_img_base64 = base64.b64encode(encoded_img_bytes).decode('utf-8')

        image_data_bytes_bysender = base64.b64decode(combined_img_base64)
        image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
        top_image_section = Get_Top_image(image_bysender, 200)
        decoded_msg = retrieve_message(top_image_section)
        print("msgextracted>>>>>>>>>>>:", decoded_msg)

        # Add data URI scheme to the base64 string
        data_uri = f"data:image/{image_data_base64_bysender_type};base64,{combined_img_base64}"
        print("final url created")
        socketio.emit( chanel_sender, {'status': 'true', 'message':'', 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':data['file']})
        socketio.emit( chanel_receiver, {'status': 'true', 'message':'', 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':data_uri})

@socketio.on('decrypt_message_com') 
def handle_video_and_task(data):
    print("decryption started")
    global values, user_actions, isResult   
    senderId = data.get('senderID')
    video_frame = data.get('videoFrame')
    base64_text = re.search(r"data:image/jpeg;base64,(.*)", video_frame).group(1)
    image_data = base64.b64decode(base64_text)
    image2 = Image.open(BytesIO(image_data))
    print("videor frame captured")
    facialFeatureExtractor = FacialFeatureExtractor()
    facialFeatures =  facialFeatureExtractor.capture_image_and_encoding("Registering your face. Press 'Enter' when ready...", image2)
 
    image_data_base64_bysender = data['file'].split(',')[1]  # remove the 'data:image/png;base64,' prefix
    image_data_base64_bysender_type = data['file'].split(',')[0].split(';')[0].split('/')[-1]
    image_data_bytes_bysender = base64.b64decode(image_data_base64_bysender)
    image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
    profile_data_sender=get_profile_data_by_guid(senderId)
    encodedVault_sender=profile_data_sender[3]
    vault_sender=decode_object(encodedVault_sender)
    loginResult=vault_sender.verify_user_and_get_password(facialFeatures)  
    if(loginResult is None):
        print("loginResult:", loginResult)
        socketio.emit(senderId, {'file':'','status': 'false'})
        return
    print("loginResult:", loginResult) 
    key_sender = loginResult
    print("key_sender:", key_sender)
    top_image_section = Get_Top_image(image_bysender, 200)

    decoded_msg = retrieve_message(top_image_section)
    print("msgextracted:", decoded_msg)
    msgextracted= json.loads(decoded_msg)
    print("msgextracted:", msgextracted)
    imgHeader,imgEncrypted=split_images(image_bysender,msgextracted['height1'],msgextracted['height2'] )
    print("key_sender:", key_sender)
    decoded_msg = retrieve_message(imgHeader)

    msgextracted= json.loads(decoded_msg)
    msgobjRecovered = Message()
    msgobjRecovered.__dict__ = msgextracted
    stored_password2 = np.array(key_sender)
    password_list = stored_password2.astype(str).tolist()
    password_string = "".join(password_list)
    decrypted_img = decrypt_image(imgEncrypted, password_string)
    decrypted_img_byte_array = io.BytesIO()
    decrypted_img.save(decrypted_img_byte_array, format=image_data_base64_bysender_type)
    encoded_img_bytes = decrypted_img_byte_array.getvalue()
    decrypted_img_base64 = base64.b64encode(encoded_img_bytes).decode('utf-8')
    # Add data URI scheme to the base64 string
    data_uri = f"data:image/{image_data_base64_bysender_type};base64,{decrypted_img_base64}"
    socketio.emit(senderId, {'file':data_uri,'status': 'true'})

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











 





