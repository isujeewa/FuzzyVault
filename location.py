import hashlib

def calculate_tolerance_radius(toleration_distance_km):
    # Convert toleration_distance to degrees
    toleration_radius_degrees = toleration_distance_km / 111.32
    return toleration_radius_degrees

def generate_unique_key(latitude, longitude, toleration_distance=2.0):
    # Convert toleration_distance to degrees
    toleration_radius_degrees = calculate_tolerance_radius(toleration_distance)

    # Round coordinates based on toleration_distance
    rounded_latitude = round(latitude / toleration_radius_degrees) * toleration_radius_degrees
    rounded_longitude = round(longitude / toleration_radius_degrees) * toleration_radius_degrees

    # Combine rounded coordinates for uniqueness
    combined_data = f"{rounded_latitude}:{rounded_longitude}"

    # Use hashlib to generate a unique key
    unique_key = hashlib.sha256(combined_data.encode()).hexdigest()

    return unique_key

# Example usage
latitude_user1 =6.902824012349254
longitude_user1 =79.85450551168583

latitude_user2 =6.90154479393716
longitude_user2 =79.85158859849618

# Users within 2 km
toleration_distance_km = 2.0
toleration_radius_degrees = calculate_tolerance_radius(toleration_distance_km)

unique_key_user1 = generate_unique_key(latitude_user1, longitude_user1, toleration_distance=toleration_distance_km)
unique_key_user2 = generate_unique_key(latitude_user2, longitude_user2, toleration_distance=toleration_distance_km)

print(f"Toleration Distance Radius in Degrees: {toleration_radius_degrees}")
print(f"User 1 Unique Key: {unique_key_user1}")
print(f"User 2 Unique Key: {unique_key_user2}")
