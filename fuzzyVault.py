import numpy as np
import face_recognition
import cv2
import skfuzzy as fuzz

class FuzzyVault:
    _private_secret = ""  # Class-level private variable
    _stored_face_encoding = []  # Class-level private variable

    def __init__(self):
        # Initialize variables properly
        self._private_secret = ""
        self._stored_face_encoding = None

    @staticmethod
    def __generate_random_password():
        # Generate a random password
        random_password = np.arange(20)
        np.random.shuffle(random_password)
        # Convert the password to a string
        random_password_str = ''.join(map(str, random_password))
        random_password_str = np.array([int(x) for x in random_password_str])
        # Use "12345" as the password for fuzzification
        stored_password = random_password_str
        # Convert the NumPy array to a list of strings
        password_list = stored_password.astype(str).tolist()
        # Convert the list to a plain string
        password_string = "".join(password_list)
        return password_string
    
    def register_user(self, face_encoding: np.ndarray):
        # Assign values to class variables
        self._private_secret = self.__generate_random_password()
        self._stored_face_encoding = face_encoding

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
