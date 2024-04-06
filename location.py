import hashlib
from scipy.stats import chisquare

def calculate_tolerance_radius(toleration_distance_km):
    # Convert toleration_distance to degrees
    toleration_radius_degrees = toleration_distance_km / 111.32
    return toleration_radius_degrees

def generate_unique_key(latitude, longitude, toleration_distance=2.0):
    print("generate_unique_key....")
    print("latitude",latitude)
    print("longitude",longitude)
    print("toleration_distance",toleration_distance)
    # Convert toleration_distance to degrees
    toleration_radius_degrees = calculate_tolerance_radius(toleration_distance)

    # Round coordinates based on toleration_distance
    rounded_latitude = round(latitude / toleration_radius_degrees) * toleration_radius_degrees
    rounded_longitude = round(longitude / toleration_radius_degrees) * toleration_radius_degrees

    # Combine rounded coordinates for uniqueness
    combined_data = f"{rounded_latitude}:{rounded_longitude}"

    # Use hashlib to generate a unique key
    unique_key = hashlib.sha256(combined_data.encode()).hexdigest()

    print("generate_unique_key end....")

    return unique_key



def evaluate_randomness(key):
    # Convert hexadecimal key to a list of integers
    key_integers = [int(key[i:i+2], 16) for i in range(0, len(key), 2)]
    
    # Perform the chi-squared test
    _, p_value = chisquare(key_integers)
    
    return p_value

# Example keys (replace these with your actual keys)
key1 = "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6"
key2 = "6c5b4a3d2e1c0b9a8f7e6d5c4b3a2f1"

# Evaluate randomness for each key
p_value1 = evaluate_randomness(key1)
p_value2 = evaluate_randomness(key2)

# Print the p-values
print("P-value for Key 1:", p_value1)
print("P-value for Key 2:", p_value2)

# Example usage
latitude_user1 =6.848512
longitude_user1 =79.8476

latitude_user2 =6.848512
longitude_user2 =79.8818304

# Users within 2 km
toleration_distance_km = 3.0
toleration_radius_degrees = calculate_tolerance_radius(toleration_distance_km)

unique_key_user1 = generate_unique_key(latitude_user1, longitude_user1, toleration_distance=toleration_distance_km)
unique_key_user2 = generate_unique_key(latitude_user2, longitude_user2, toleration_distance=toleration_distance_km)

print(f"Toleration Distance Radius in Degrees: {toleration_radius_degrees}")
print(f"Location 1: {latitude_user1},{longitude_user1}")
print(f"Location 2: {latitude_user2},{longitude_user2}")

print(f"Location 1 Key: {unique_key_user1}")
print(f"Location 2 Key: {unique_key_user2}")
print(f"Keys Match: {unique_key_user1 == unique_key_user2}")
#check the randomness of the key
p_value_user1 = evaluate_randomness(unique_key_user1)
p_value_user2 = evaluate_randomness(unique_key_user2)
print("A lower P-value indicates less randomness")
print("P-value for User 1 Key:", p_value_user1)
print("P-value for User 2 Key:", p_value_user2)
