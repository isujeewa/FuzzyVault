import cv2
import face_recognition
import numpy as np
import skfuzzy as fuzz

def capture_image_and_encoding():
    print("Please look straight. Press 'Enter' when ready.")
    input("Press Enter to capture...")

    cap = cv2.VideoCapture(0)

    # Wait for a brief moment to allow the camera to stabilize
    cv2.waitKey(1000)

    # Capture a frame
    ret, frame = cap.read()

    # Convert the frame to RGB for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(rgb_frame)

    if face_locations:
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
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

# Function to verify the user and return the correct password
def verify_user_and_get_password(user_encoding, stored_encoding, stored_password):
    # Compare facial encodings for verification
    face_distance = face_recognition.face_distance([stored_encoding], user_encoding)[0]

    # You may need to adjust the threshold based on your specific use case
    threshold = 0.4

    if face_distance < threshold:
        return stored_password
    else:
        return None

# Example usage
def main():
    # Capture facial features
    face_encoding = capture_image_and_encoding()

    # Use "12345" as the password for fuzzification
    stored_password = np.array([0, 4, 6, 8, 1,2])

    stored_encoding = face_encoding  # Store the initial facial encoding

    # Fuzzify facial features
    fuzzified_values = fuzzify_features(face_encoding)

    print("Fuzzified Values:", fuzzified_values)
    

    # Allow the user to capture another snapshot for verification
    input("\nPress Enter to capture another snapshot for verification...")

    # Capture the second snapshot for verification
    verification_encoding = capture_image_and_encoding()

    # Verify the user and get the correct password
    correct_password = verify_user_and_get_password(verification_encoding, stored_encoding, stored_password)

    if correct_password is not None:
        print("User Verified! Correct Password:", correct_password)
    else:
        print("User Verification Failed! Incorrect Password.")

if __name__ == "__main__":
    main()
