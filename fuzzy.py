import numpy as np
import face_recognition
import cv2
import skfuzzy as fuzz


def capture_image_and_encoding(msg):
    print("Please look straight.")


    cap = cv2.VideoCapture(0)

    # Wait for a brief moment to allow the camera to stabilize
    cv2.waitKey(1000)

    # Capture frames from the camera until a face is detected
    ret, frame = cap.read()

    # Convert captured frames to RGB for face recognition
    rgb_frame_captured = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings
    face_featue_locations = face_recognition.face_locations(rgb_frame_captured)

    if face_featue_locations:
        face_encoding = face_recognition.face_encodings(rgb_frame_captured, face_featue_locations)[0]
        print("Image Captured!")

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

        return face_encoding

# Function to fuzzify the facial features
def fuzzify_features(face_encoding):
    # Fuzzify the face_encoding values
    fuzzified_values = fuzz.trapmf(face_encoding, [0, 0, 0.2, 0.5])

    return fuzzified_values

class UserVerificationError(Exception):
    pass

# Function to verify the user and return the correct password
def verify_user_and_get_password(user_encoding, stored_encoding, stored_password):
    try:
        # Compare facial encodings for verification
        face_distance = face_recognition.face_distance([stored_encoding], user_encoding)[0]

        # You may need to adjust the threshold based on your specific use case
        threshold = 0.4

        if face_distance < threshold:
            return stored_password
        else:
            return None
    except Exception as e:
        # Handle exceptions specific to your application
        #write error to log
        #print(f"Error during user verification: {str(e)}")
        return "-1" #UserVerificationError(f"Error during user verification: {str(e)}")

