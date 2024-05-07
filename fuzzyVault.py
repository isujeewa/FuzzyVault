import numpy as np
import face_recognition

class FuzzyVault:
    _private_secret = ""  # Class-level private variable
    _stored_face_encoding = []  # Class-level private variable
    _public_key = None  # Class-level private variable

    def __init__(self):
        # Initialize variables properly
        self._private_secret = ""
        self._stored_face_encoding = None

   
    def register_user(self,privateKey:str, face_encoding: np.ndarray):
        # Assign values to class variables
        self._private_secret = privateKey
        self._stored_face_encoding = face_encoding

    def setPublicKey(self, key: str):
        # Assign values to class variables
        self._public_key =key
    def getPublicKey(self):
        return self._public_key

    def get_key(self ):
        return self._private_secret

    def verify_user_and_get_password(self, user_encoding: np.ndarray) -> str:
        try:
            print("Verifying user...")
            # Compare facial encodings for verification
            face_distance = face_recognition.face_distance([self._stored_face_encoding], user_encoding)[0]
            # You may need to adjust the threshold based on your specific use case
            threshold = 0.6
            if face_distance < threshold:
                return self._private_secret
            else:
                return None
        except Exception as e:
            # Handle exceptions
            # Log error
            print(f"Error during user verification: {str(e)}")
            return "-1"
