import hashlib

import numpy as np

def generate_random_password():
    # Generate a random password
    random_password = np.arange(20)
    np.random.shuffle(random_password)

    # Convert the password to a string
    random_password_str = ''.join(map(str, random_password))

    random_password_str = np.array([int(x) for x in random_password_str])

    return random_password_str