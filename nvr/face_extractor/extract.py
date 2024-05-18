import os
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurable variables
API_URL = "http://localhost:8000/api/v1/detection/detect"
API_KEY = os.getenv("API_KEY")
INPUT_DIR = "input_photos"
OUTPUT_DIR = "output_faces"
PROBABILITY_THRESHOLD = 0.8
MAX_SIZE = 300
SUPPORTED_EXTENSIONS = {'.jpeg', '.jpg', '.png', '.webp'}
EXPANSION_FACTOR = 0.10

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to resize the image while maintaining aspect ratio
def resize_image(image, max_size):
    width, height = image.size
    if width > max_size or height > max_size:
        scaling_factor = min(max_size / width, max_size / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.LANCZOS)
    return image

# Iterate over each image in the input directory
for image_name in os.listdir(INPUT_DIR):
    image_path = os.path.join(INPUT_DIR, image_name)

    # Check if the file has a supported extension
    if os.path.isfile(image_path) and os.path.splitext(image_path)[1].lower() in SUPPORTED_EXTENSIONS:
        print(f"Processing {image_path}...")

        # Send the image to the Compreface detect API
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                API_URL,
                headers={'x-api-key': API_KEY},
                files={'file': image_file}
            )

        # Check if the request was successful
        if response.status_code == 200:
            results = response.json().get('result', [])

            # Get the filename without extension
            filename, _ = os.path.splitext(image_name)

            # Open the original image
            with Image.open(image_path) as img:
                img_width, img_height = img.size
                for index, result in enumerate(results):
                    probability = result.get('box', {}).get('probability', 0)

                    if probability > PROBABILITY_THRESHOLD:
                        box = result.get('box', {})
                        x_min = box.get('x_min')
                        x_max = box.get('x_max')
                        y_min = box.get('y_min')
                        y_max = box.get('y_max')

                        # Calculate expansion offsets
                        expand_x = int((x_max - x_min) * EXPANSION_FACTOR)
                        expand_y = int((y_max - y_min) * EXPANSION_FACTOR)

                        # Recalculate the coordinates
                        x_min = max(x_min - expand_x, 0)
                        x_max = min(x_max + expand_x, img_width)
                        y_min = max(y_min - expand_y, 0)
                        y_max = min(y_max + expand_y, img_height)

                        # Crop the face from the original image with the expanded coordinates
                        face = img.crop((x_min, y_min, x_max, y_max))

                        # Resize the face image to a maximum size
                        face = resize_image(face, MAX_SIZE)
                        face.save(os.path.join(OUTPUT_DIR, f"{filename}_face_{index}.jpg"))
        else:
            print(f"Failed to process {image_path}, status code: {response.status_code}")
    else:
        print(f"{image_path} is not a supported file type, skipping...")
