import io
import json
import os
import numpy as np
from RSAKeyPair import  decrypt_message, deserialize_public_key, encrypt_message, generate_keys, serialize_private_key, serialize_public_key
import base64
from io import BytesIO
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from location import generate_unique_key
from message import Message
from steganography import hide_message, retrieve_message
from steganographyv4 import encode, decode
from imageGen import Get_Top_image, calculate_text_width,   create_banner,combine_images, create_image,split_images
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
socketio = SocketIO(app, cors_allowed_origins='*',max_http_buffer_size=2e7)

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
        socketio.emit('result_registration', {'status': 'false'})
        return
    else:
        private_key, public_key =generate_keys()
        private_pem = serialize_private_key(private_key)
        public_pem = serialize_public_key(public_key)
        print("public_pem:", public_pem)
        print("private_pem:", private_pem)
        fuzzy_vault = FuzzyVault()
        fuzzy_vault.setPublicKey(public_pem)
        fuzzy_vault.register_user(private_pem, facialFeatures)
        strend=encode_object(fuzzy_vault)

        #get new guid
         # Generate a UUID
        new_uuid = uuid.uuid4()
        # Convert the UUID to a string
        new_uuid_str = str(new_uuid)
        msg=insert_profile_data(new_uuid_str,name, email, strend)
        socketio.emit('result_registration', {'status': 'true','msg':msg})
        # Show the image

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
    if(profile_data is None):
        socketio.emit('result_login', {'status': 'false'})
        return
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
        socketio.emit('result_login', {'status': 'false'})
        return
    socketio.emit('result_login', {'status': 'true','guid':profile_data[0], 'name':profile_data[1], 'email':profile_data[2]})
    
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
    print("-----------------------Send -------------------")   
    senderId = data.get('senderID')
    receiverId = data.get('receiverID')
    message = data.get('message')
    encryptionOption = data.get('encryptionOption')
    fileName = data.get('fileName')
    type = data.get('type')
    time = data.get('time')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    distance = data.get('distance')
    encryptTextMessage = data.get('encryptTextMessage')
    chanel_sender = f"{senderId}_{receiverId}"
    chanel_receiver = f"{receiverId}_{senderId}"
    print("chanel_sender:", chanel_sender)
    print("chanel_receiver:", chanel_receiver)
    print("encryptionOption:", encryptionOption)
    print("longitude--:", longitude)
    print("latitude--:", latitude)
    print("distance--:", distance)
    print("encryptTextMessage" ,encryptTextMessage)
    if message is None:
        message=""

    print("type:", type)
    #base64_text = re.search(r"data:image/png;base64,(.*)", file).group(1)
    #split by coma
    if type =='0':
        
        socketio.emit( chanel_sender, {'status': 'true', 'message':message, 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':'','encryptionOption':'0'})
        socketio.emit( chanel_receiver, {'status': 'true', 'message':message, 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':'','encryptionOption':'0'})
    if type =='1':
        #cooment image received
        image_data_base64_bysender= None
        image_data_base64_bysender_type= None
        image_data_bytes_bysender= None
        image_bysender= None
        imageFile= None
        banner_text = None
        print("encryptTextMessage" ,encryptTextMessage)
        if(encryptTextMessage != True):
            print("encryptTextMessage")
            image_data_base64_bysender = data['file'].split(',')[1]  # remove the 'data:image/png;base64,' prefix
            image_data_base64_bysender_type = data['file'].split(',')[0].split(';')[0].split('/')[-1]
            imageFile = data['file']
            print("image received")
            image_data_bytes_bysender = base64.b64decode(image_data_base64_bysender)
            image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
            banner_text = message
        else:
            widthText = calculate_text_width(message, 12)
            image_bysender =create_image(widthText, 200, message)
            fileName="Secret Message"
            image_data_base64_bysender_type="png"
            message_img_byte_array = io.BytesIO()
            image_bysender.save(message_img_byte_array, format=image_data_base64_bysender_type)
            encoded_img_bytes = message_img_byte_array.getvalue()
            message_img_base64 = base64.b64encode(encoded_img_bytes).decode('utf-8')
            imageFile = f"data:image/{image_data_base64_bysender_type};base64,{message_img_base64}"
            banner_text=" "
        if encryptionOption =='0' and encryptTextMessage != True:
            #TODO handle encrypted image
            socketio.emit( chanel_sender, {'status': 'true', 'message':'', 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':data['file'],'encryptionOption':'0'})
            socketio.emit( chanel_receiver, {'status': 'true', 'message':'', 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':data['file'],'encryptionOption':'0'})
            return
        elif encryptionOption =='1' :


            print("processed the image")
            profile_data_receiver=get_profile_data_by_guid(receiverId)
            encodedVault_receiver =profile_data_receiver[3]
            vault_receiver=decode_object(encodedVault_receiver)   
            key_receiver_publickey = vault_receiver.getPublicKey()
            print("vault created")

            height = 200
            width =  image_bysender.width
            print("width:", width)
            print("height:", height)
            print("fileName:", fileName)
            print("message:", message)
            banner_img=create_banner(width, height, fileName, banner_text)
      
            print("banner_img created")
           
            #generate a random key
            randomKey = keyGeneration.generate_random_key()
            randomKeyString = keyGeneration.get_string_from_array(randomKey)
            deserialized_public_key = deserialize_public_key(key_receiver_publickey)
            encrypted_key = encrypt_message(deserialized_public_key, randomKeyString)
            encrypted_key_base64 = base64.b64encode(encrypted_key).decode('utf-8') 
            #encrypt the image with the key
            encrypted_img = encrypt_image(image_bysender, randomKeyString)

            print("encrypted_img created")
            # Create a message object and serialize it to JSON
            msgobj = Message()
            #msgobj.secret = key_receiver
            #last 4 digit of the key_receiver
            msgobj.encryptedKey = encrypted_key_base64
            msgobj.secret = randomKeyString[-4:]
            msgobj.height1 = banner_img.height
            msgobj.height2 = encrypted_img.height
            msgobj.authOption = 1
            msgorg = json.dumps(msgobj.__dict__)
        
            print("message created ")
            #encoded_img = hide_message(banner_img, msgorg)
            encoded_img = encode(banner_img, msgorg)
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
            #decoded_msg = retrieve_message(top_image_section)
            decoded_msg = decode(top_image_section)

            # Add data URI scheme to the base64 string
            data_uri = f"data:image/{image_data_base64_bysender_type};base64,{combined_img_base64}"
            print("final url created for bio encrypted image")
            socketio.emit( chanel_sender, {'status': 'true', 'message':'', 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':imageFile,'encryptionOption':encryptionOption})
            socketio.emit( chanel_receiver, {'status': 'true', 'message':'', 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':data_uri,'encryptionOption':encryptionOption})
        elif encryptionOption =='2' : 
            print("image received")
            print(latitude, longitude)
            key_receiver=generate_unique_key(float(latitude), float(longitude), toleration_distance=float(distance))
            print("key_receiver:", key_receiver)
            image_data_bytes_bysender = base64.b64decode(image_data_base64_bysender)
            image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
            encrypted_img2 = encrypt_image(image_bysender, key_receiver)
            height = 200
            width =  image_bysender.width
            banner_img=create_banner(width, height, fileName, banner_text)
            print(image_bysender.filename)
            print("banner_img created")
  
            msgobj = Message()
            #msgobj.secret = key_receiver
            #last 4 digit of the key_receiver
            msgobj.secret = key_receiver[-4:]
            msgobj.height1 = banner_img.height
            msgobj.height2 = encrypted_img2.height
            msgobj.authOption = 2
            msgobj.distance = distance
            msgorg = json.dumps(msgobj.__dict__)
        
            print("message created ")
            #encoded_img = hide_message(banner_img, msgorg)
            encoded_img = encode(banner_img, msgorg)
            print("added message to image")
            
            combined_img_loc= combine_images(encoded_img, encrypted_img2)
            
            print("combined image created")
    
            print("file_type:", image_data_base64_bysender_type)
            # Convert the image to bytes and then encode to base64
            combined_img_byte_array_loc = io.BytesIO()
            combined_img_loc.save(combined_img_byte_array_loc, format=image_data_base64_bysender_type)
            encoded_img_bytes_loc = combined_img_byte_array_loc.getvalue()
            combined_img_base64_loc = base64.b64encode(encoded_img_bytes_loc).decode('utf-8')
            data_uri_loc = f"data:image/{image_data_base64_bysender_type};base64,{combined_img_base64_loc}"
            socketio.emit( chanel_sender, {'status': 'true', 'message':'', 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':imageFile,'encryptionOption':encryptionOption})
            socketio.emit( chanel_receiver, {'status': 'true', 'message':'', 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':data_uri_loc,'encryptionOption':encryptionOption})
        elif encryptionOption =='3' :
            print("image received option:3")

            profile_data_receiver=get_profile_data_by_guid(receiverId)
            encodedVault_receiver =profile_data_receiver[3]
            vault_receiver=decode_object(encodedVault_receiver)   
            key_receiver_publickey = vault_receiver.getPublicKey()

            #generate a random key
            randomKey = keyGeneration.generate_random_key()
            randomKeyString = keyGeneration.get_string_from_array(randomKey)
            deserialized_public_key = deserialize_public_key(key_receiver_publickey)
            encrypted_key = encrypt_message(deserialized_public_key, randomKeyString)
            encrypted_key_base64 = base64.b64encode(encrypted_key).decode('utf-8') 

            key_receiver_2=generate_unique_key(float(latitude), float(longitude), toleration_distance=float(distance))
            combined_key=randomKeyString+key_receiver_2
            last_8_digit=randomKeyString[-4:]+key_receiver_2[-4:]
            print("vault created")

            height = 200
            width =  image_bysender.width
            banner_img=create_banner(width, height, fileName ,banner_text)
            print("banner_img created")
            # Create a message object and serialize it to JSON
            encrypted_img = encrypt_image(image_bysender, combined_key)
            print("encrypted_img created")
            msgobj = Message()
            #msgobj.secret = key_receiver
            #last 4 digit of the key_receiver
            msgobj.encryptedKey = encrypted_key_base64
            msgobj.secret = last_8_digit
            msgobj.height1 = banner_img.height
            msgobj.height2 = encrypted_img.height
            msgobj.authOption = 3
            msgobj.distance = distance
            msgorg = json.dumps(msgobj.__dict__)
        
            print("message created ")
            #encoded_img = hide_message(banner_img, msgorg)
            encoded_img = encode(banner_img, msgorg)
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
            #decoded_msg = retrieve_message(top_image_section)
            decoded_msg = decode(top_image_section)

            # Add data URI scheme to the base64 string
            data_uri = f"data:image/{image_data_base64_bysender_type};base64,{combined_img_base64}"
            print("final url created for bio encrypted image")
            socketio.emit( chanel_sender, {'status': 'true', 'message':'', 'time':time ,'senderID':senderId, 'receiverID':receiverId, 'file':imageFile,'encryptionOption':encryptionOption})
            socketio.emit( chanel_receiver, {'status': 'true', 'message':'', 'time':time,'senderID':senderId, 'receiverID':receiverId,'file':data_uri,'encryptionOption':encryptionOption})
    print("-----------------------Send End-------------------")  


@socketio.on('decrypt_message_com') 
def handle_video_and_task(data):
    global values, user_actions, isResult   
    print("-----------------------decrypt -------------------")
    encryptionOption = data.get('encryptionOption')
    receiverID = data.get('receiverID')

 
    image_data_base64_bysender = data['file'].split(',')[1]  # remove the 'data:image/png;base64,' prefix
    image_data_base64_bysender_type = data['file'].split(',')[0].split(';')[0].split('/')[-1]
    image_data_bytes_bysender = base64.b64decode(image_data_base64_bysender)
    image_bysender = Image.open(BytesIO(image_data_bytes_bysender))
    loginResult=None
    
    top_image_section = Get_Top_image(image_bysender, 200)

    #decoded_msg = retrieve_message(top_image_section)
    decoded_msg = decode(top_image_section)
    print("msgextracted:", decoded_msg)
    msgextracted= json.loads(decoded_msg)
    print("msgextracted:", msgextracted)
    msgobjRecovered = Message()
    msgobjRecovered.__dict__ = msgextracted
    encryptedKey =""
    key = None
    decrypted_key = ""

    imgHeader,imgEncrypted=split_images(image_bysender,msgextracted['height1'],msgextracted['height2'] )
    print("encryptionOption:", encryptionOption)
    #decoded_msg = retrieve_message(imgHeader)
    decoded_msg = decode(imgHeader)
    print("msgextracted:", decoded_msg)
    if encryptionOption =='1' :
        video_frame = data.get('videoFrame')
        base64_text = re.search(r"data:image/jpeg;base64,(.*)", video_frame).group(1)
        image_data = base64.b64decode(base64_text)
        image2 = Image.open(BytesIO(image_data))
    
        print("videor frame captured")
        facialFeatureExtractor = FacialFeatureExtractor()
        facialFeatures =  facialFeatureExtractor.capture_image_and_encoding("...", image2)
        if(facialFeatures is None):
            print("loginResult:", facialFeatures)
            socketio.emit(receiverID, {'file':'F','status': 'false'})
            return
        print("face based:")
        
        profile_data_receiver=get_profile_data_by_guid(receiverID)
        encodedVault_reciver=profile_data_receiver[3]
        vault_receiver=decode_object(encodedVault_reciver)
        loginResult=vault_receiver.verify_user_and_get_password(facialFeatures)

        if(loginResult is None):
            print("loginResult:", loginResult)
            socketio.emit(receiverID, {'file':'F','status': 'false'})
            return
        encryptedKey = base64.b64decode(msgobjRecovered.encryptedKey)
        print("encryptedKey:", encryptedKey)
        print("privatekey:", loginResult)
        decrypted_key = decrypt_message( loginResult,encryptedKey)
        print("decrypted_key:", decrypted_key)
        key_receiver = decrypted_key

    elif encryptionOption =='2' :
        print("location based:")
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        print("longitude:", longitude)
        print("latitude:", latitude)
        print("distance:", msgextracted["distance"])
        loginResult=generate_unique_key(float(latitude), float(longitude), toleration_distance=float(msgextracted["distance"]))
        print("loginResult:", loginResult)
        key_receiver = loginResult
        print("sec:", msgextracted["secret"])
        print("key_receiver[-4]:", key_receiver[-4:])
        if msgextracted["secret"] !=  key_receiver[-4:] :
            socketio.emit(receiverID, {'file':'','status': 'false'})
            print("Error: Location mismatch.")
            return
    elif encryptionOption =='3' :
        video_frame = data.get('videoFrame')
        base64_text = re.search(r"data:image/jpeg;base64,(.*)", video_frame).group(1)
        image_data = base64.b64decode(base64_text)
        image2 = Image.open(BytesIO(image_data))
    
        print("videor frame captured")
        facialFeatureExtractor = FacialFeatureExtractor()
        facialFeatures =  facialFeatureExtractor.capture_image_and_encoding("Registering your face. Press 'Enter' when ready...", image2)
        if(facialFeatures is None):
            print("loginResult:", facialFeatures)
            socketio.emit(receiverID, {'file':'F','status': 'false'})
            return
        
        print("face based:")
        
        profile_data_sender=get_profile_data_by_guid(receiverID)
        encodedVault_sender=profile_data_sender[3]
        vault_sender=decode_object(encodedVault_sender)
        loginResult_1=vault_sender.verify_user_and_get_password(facialFeatures)
        if(loginResult_1 is None):
            print("loginResult:", loginResult_1)
            socketio.emit(receiverID, {'file':'','status': 'false'})
            return
        encryptedKey = base64.b64decode(msgobjRecovered.encryptedKey)
        print("encryptedKey:", encryptedKey)
        print("privatekey:", loginResult)
        decrypted_key = decrypt_message( loginResult_1,encryptedKey)
        longitude = data.get('longitude')
        latitude = data.get('latitude')
        print("longitude:", longitude)
        print("latitude:", latitude)
        print("distance:", msgextracted["distance"])
        loginResult_2=generate_unique_key(float(latitude), float(longitude), toleration_distance=float(msgextracted["distance"]))
        org_location_key_part= loginResult_2[-4:]
        org_face_key_part= decrypted_key[-4:]
        key_receiver = decrypted_key+loginResult_2
        #get string from last 68-64
        key_part =msgextracted["secret"][-4:]
        print("sec:", msgextracted["secret"])
        
        if key_part != org_location_key_part :
            socketio.emit(receiverID, {'file':'L','status': 'false'})
            print("Error: Location mismatch.")
            return 
        key_part =msgextracted["secret"][:4]
        if key_part != org_face_key_part :
            socketio.emit(receiverID, {'file':'F','status': 'false'})
            print("Error: face mismatch.")
            return 
    

    stored_password2 = np.array(key_receiver)
    password_list = stored_password2.astype(str).tolist()
    password_string = "".join(password_list)

    decrypted_img = decrypt_image(imgEncrypted, password_string)
    decrypted_img_byte_array = io.BytesIO()
    decrypted_img.save(decrypted_img_byte_array, format=image_data_base64_bysender_type)
    encoded_img_bytes = decrypted_img_byte_array.getvalue()
    decrypted_img_base64 = base64.b64encode(encoded_img_bytes).decode('utf-8')
    # Add data URI scheme to the base64 string
    data_uri = f"data:image/{image_data_base64_bysender_type};base64,{decrypted_img_base64}"
    socketio.emit(receiverID, {'file':data_uri,'status': 'true'})
    print("-----------------------decrypt End-------------------")

if __name__ == '__main__':
    socketio.run(app, debug=True)
    #log
    print("Server started")













 





