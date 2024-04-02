import numpy as np
import face_recognition
import cv2
import skfuzzy as fuzz
from PIL import Image 

class FacialFeatureExtractor:
    def __init__(self):
        pass
    def capture_image_and_encoding(self, msg :str ,image: Image):
        print("Please look straight.")
   

        # Capture the image
        image_np = np.array(image)
        # Convert captured frames to RGB for face recognition
        rgb_frame_captured = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        # Find face locations and encodings
        face_featue_locations = face_recognition.face_locations(rgb_frame_captured)
        if face_featue_locations:
            face_encoding = face_recognition.face_encodings(rgb_frame_captured, face_featue_locations)[0]
            print("Image Captured!")

            cv2.destroyAllWindows()

            return face_encoding
        else:
            print("No face detected. Please try again.")
            return None