from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2

def mse(imageA, imageB):
    # Calculate the Mean Squared Error between two images.
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def compare_images(imageA, imageB):
    # Calculate the MSE and SSIM
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return m, s

def main():
    # Define the image paths
    path01= "Testing\\decrypted_img.png"
    path02= "Testing\\originalimage.png"

    # Load images from specified paths
    image1 = cv2.imread(path01)
    image2 = cv2.imread(path02)

    if image1 is None or image2 is None:
        print("One of the image paths is invalid. Please check the paths and try again.")
        return

    # Convert the images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            
    # Check for the same size and aspect ratio, and report accordingly
    ho, wo = gray1.shape
    hc, wc = gray2.shape
    ratio_orig = ho / wo
    ratio_comp = hc / wc

    if round(ratio_orig, 2) != round(ratio_comp, 2):
        print("Images do not have the same aspect ratio. Please provide images with the same dimensions.")
        return

    # Resize images to the same dimensions if necessary
    if ho != hc or wo != wc:
        gray2 = cv2.resize(gray2, (wo, ho))

    # Compare images using MSE and SSIM
    mse_value, ssim_value = compare_images(gray1, gray2)

    print(f"MSE: {mse_value}")
    print(f"SSIM: {ssim_value}")

if __name__ == "__main__":
    main()
