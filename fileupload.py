from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import requests
from PIL import Image
from io import BytesIO

account_name = "snapsecure"
account_key = "cKeQuzhIOZVUrg74HENk5Y7xuO4EOdrsRc8rNfhhDhUZM/3EptiWtBUoASAiiVmBMrX0VtUqij2i+AStwoervQ=="
container_name = "chatimgs"

blob_service_client = BlobServiceClient(
    account_url=f"https://{account_name}.blob.core.windows.net",
    credential=account_key
)
container_client = blob_service_client.get_container_client(container_name)


def upload_image_to_blob(image_path, blob_name):
    blob_client = container_client.get_blob_client(blob_name)
    with open(image_path, "rb") as data:
        blob_client.upload_blob(data)

def get_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        return image
    else:
        print(f"Failed to download image from URL: {image_url}")
        return None

# Example usage:
image_url = "https://snapsecure.blob.core.windows.net/chatimgs/test.png"
image = get_image_from_url(image_url)
if image:
    print("Image successfully downloaded and converted to Image object.")
    # Now you can use the 'image' object as a PIL Image object
else:
    print("Failed to download and convert image.")

image_path = "C:\\female.png"
blob_name = "test2.png"
upload_image_to_blob(image_path, blob_name)