import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import numpy as np
import cv2

def dhash(image, hash_size=8):
    # Convert the image to grayscale
    image = image.convert('L')
    
    # Resize the image to (hash_size + 1) x hash_size
    image = image.resize((hash_size + 1, hash_size), Image.LANCZOS)
    
    # Calculate the difference between adjacent pixel values
    difference = []
    for y in range(hash_size):
        for x in range(hash_size):
            pixel_left = image.getpixel((x, y))
            pixel_right = image.getpixel((x + 1, y))
            difference.append(pixel_left > pixel_right)
    
    # Convert the binary difference list to a hexadecimal hash string
    hash_value = ''.join(['1' if bit else '0' for bit in difference])
    hash_hex = hex(int(hash_value, 2))[2:].rjust(hash_size // 4, '0')
    
    return hash_hex

# def hamming_distance(hash1, hash2):
#     assert len(hash1) == len(hash2)
#     distance = sum(bit1 != bit2 for bit1, bit2 in zip(hash1, hash2))
#     hash_size = len(hash1) * 4  # Each hex digit represents 4 bits
#     max_distance = hash_size  # Maximum possible Hamming distance
#     hash_percentage = ((max_distance - distance) / max_distance) * 100
#     return hash_percentage

def compare_shapes(image1, image2):
    # Get the dimensions of the images
    shape1 = image1.size
    shape2 = image2.size
    
    # Calculate the Euclidean distance between the shapes
    shape_distance = np.linalg.norm(np.array(shape1) - np.array(shape2))
    
    # Normalize the distance to a percentage
    max_distance = np.linalg.norm(np.array((max(shape1[0], shape2[0]), max(shape1[1], shape2[1]))))
    shape_similarity = max(0, (max_distance - shape_distance) / max_distance) * 100
    
    return shape_similarity

def compare_intensity(image1, image2):
    # Convert the images to grayscale
    grayscale1 = image1.convert('L')
    grayscale2 = image2.convert('L')
    
    # Calculate the mean intensity of each image
    intensity1 = np.mean(np.array(grayscale1))
    intensity2 = np.mean(np.array(grayscale2))
    
    # Calculate the percentage similarity in intensity
    intensity_similarity = max(0, 1 - abs(intensity1 - intensity2) / 255) * 100
    
    return intensity_similarity

def compare_colors(image1, image2):
    # Calculate the histograms of the RGB channels
    hist1 = np.histogram(np.array(image1), bins=256, range=[0, 256], density=True)
    hist2 = np.histogram(np.array(image2), bins=256, range=[0, 256], density=True)
    
    # Calculate the Bhattacharyya coefficient
    bc = np.sum(np.sqrt(hist1[0] * hist2[0]))
    
    # Calculate the percentage similarity in colors
    color_similarity = bc * 100
    
    return color_similarity

# def compare_size(image1, image2):
#     # Get the byte sizes of the images
#     size1 = image1.tell()
#     size2 = image2.tell()
    
#     # Check if the size of either image is zero
#     if size1 == 0 or size2 == 0:
#         return 0
    
#     # Calculate the percentage similarity in size
#     size_similarity = max(0, 1 - abs(size1 - size2) / max(size1, size2)) * 100
    
#     return size_similarity

def compare_blur(image1, image2):
    # Convert images to grayscale
    grayscale1 = image1.convert('L')
    grayscale2 = image2.convert('L')

    # Calculate the blur level using Laplacian variance
    blur1 = cv2.Laplacian(np.array(grayscale1), cv2.CV_64F).var()
    blur2 = cv2.Laplacian(np.array(grayscale2), cv2.CV_64F).var()

    # Normalize the blur values to a percentage
    max_blur = max(blur1, blur2)
    blur_similarity = max(0, 1 - abs(blur1 - blur2) / max_blur) * 100

    return blur_similarity

def compare_rotation_scaling(image1, image2):
    # Calculate the absolute difference in rotation and scaling
    rotation_diff = abs(image1.rotate(0).getextrema()[1][0] - image2.rotate(0).getextrema()[1][0])
    scaling_diff = abs(image1.resize(image1.size).getextrema()[1][0] - image2.resize(image2.size).getextrema()[1][0])

    # Check if the max difference is zero to avoid division by zero
    if rotation_diff == 0 and scaling_diff == 0:
        return 100  # Both rotation and scaling are the same

    # Normalize the differences to a percentage
    max_rotation_scaling_diff = max(rotation_diff, scaling_diff)
    rotation_scaling_similarity = max(0, 1 - abs(rotation_diff - scaling_diff) / max_rotation_scaling_diff) * 100

    return rotation_scaling_similarity


def compare_images(image1_path, image2_path):
    # Open images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    # Calculate dHash values
    # hash1 = dhash(image1)
    # hash2 = dhash(image2)
    
    # Calculate Hamming distance
    # hash_percentage = hamming_distance(hash1, hash2)
    
    # Calculate percentage similarity for shape, intensity, colors, size
    shape_similarity = compare_shapes(image1, image2)
    intensity_similarity = compare_intensity(image1, image2)
    color_similarity = compare_colors(image1, image2)
    # size_similarity = compare_size(image1, image2)
    
    # Additional comparisons
    blur_similarity = compare_blur(image1, image2)
    rotation_scaling_similarity = compare_rotation_scaling(image1, image2)
    
    
    # Combine the individual similarities into an overall similarity
    overall_similarity = (
         shape_similarity + intensity_similarity +
        color_similarity + blur_similarity +
        rotation_scaling_similarity
    ) / 5
    
    return overall_similarity

# Example usage:
image = "img4"
image1_path = f"result/{image}_decrypted.jpg"
image2_path = f"result/{image}.jpg"

similarity_percentage = compare_images(image1_path, image2_path)
print("Overall Similarity Percentage:", similarity_percentage)

# Plotting the results
labels = [ 'Shape', 'Intensity', 'Colors', 'Blur', 'Scale']
values = [

    compare_shapes(Image.open(image1_path), Image.open(image2_path)),
    compare_intensity(Image.open(image1_path), Image.open(image2_path)),
    compare_colors(Image.open(image1_path), Image.open(image2_path)),
    # compare_size(Image.open(image1_path), Image.open(image2_path)),
    compare_blur(Image.open(image1_path), Image.open(image2_path)),
    compare_rotation_scaling(Image.open(image1_path), Image.open(image2_path)),
    
]

fig, ax = plt.subplots()
bars = ax.bar(labels, values, color=['blue', 'green', 'orange', 'red', 'purple', 'cyan', 'magenta', 'yellow'])

ax.set_ylabel('Percentage')
ax.set_title('Image Feature Similarity: '+ image +"\n"+ f'Overall Similarity: {similarity_percentage:.2f}%')

# Adding the actual percentage value on top of the bar
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')





plt.show()
