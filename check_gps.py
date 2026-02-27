import os
from exif_extractor import get_exif_data

IMAGE_FOLDER = "images"

for image_name in os.listdir(IMAGE_FOLDER):
    image_path = os.path.join(IMAGE_FOLDER, image_name)
    print(f"\nChecking: {image_name}")

    gps, time = get_exif_data(image_path)

    if gps:
        print("GPS FOUND")
        print(gps)
        print("Timestamp:", time)
    else:
        print("No GPS data found")