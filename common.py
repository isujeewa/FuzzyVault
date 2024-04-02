import numpy as np
import base64
import pickle

def encode_object(arr):
    """
    Encode an NDArray to Base64.

    Parameters:
    arr (numpy.ndarray): The NDArray to encode.

    Returns:
    str: Base64 encoded string.
    """
    serialized_data = pickle.dumps(arr)
    encoded_data = base64.b64encode(serialized_data)
    return encoded_data.decode('utf-8')

def decode_object(encoded_data):
    """
    Decode a Base64 encoded string to NDArray.

    Parameters:
    encoded_data (str): Base64 encoded string.

    Returns:
    numpy.ndarray: Decoded NDArray.
    """
    decoded_data = base64.b64decode(encoded_data)
    arr = pickle.loads(decoded_data)
    return arr

 
