import numpy as np
import face_recognition
import cv2
from PIL import Image

class FacialFeatureExtractor:
    def __init__(self):
        pass

    def reduce_ambient_light(self, image, reduction_factor):
        """
        Reduces ambient light from an image.

        Parameters:
        - image: PIL.Image object
        - reduction_factor: A float value indicating the reduction factor (between 0 and 1).

        Returns:
        - PIL.Image object: Image with reduced ambient light.
        """
        # Convert image to numpy array for easier manipulation
        img_array = np.array(image)

        # Reduce ambient light by subtracting a scaled version of the mean
        reduced_img_array = np.clip(img_array - (reduction_factor * np.mean(img_array)), 0, 255).astype(np.uint8)

        # Convert back to PIL.Image object
        reduced_image = Image.fromarray(reduced_img_array)

        return reduced_image  
    
    def capture_image_and_encoding(self, msg: str, image: Image):
        print("Please look straight.")
   
 
        reduced_image = self.reduce_ambient_light(image, reduction_factor=0.55)
        # Capture the image
        image_np = np.array(reduced_image)  # Use reduced_image here
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
