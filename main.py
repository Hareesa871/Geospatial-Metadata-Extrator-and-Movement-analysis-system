import os
from geo_utils import get_location_name
from hybrid_landmark import infer_landmark
from exif_extractor import get_exif_data, convert_to_degrees
from landmark_detector import detect_landmark
from database import init_db, insert_data
from movement_map import generate_map
from report_generator import generate_report

IMAGE_FOLDER = "images"

init_db()

for image_name in os.listdir(IMAGE_FOLDER):
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    print(f"\nChecking: {image_name}")

    gps_data, timestamp = get_exif_data(image_path)
    print("GPS Data:", gps_data)

    if gps_data and "GPSLatitude" in gps_data:
        lat = convert_to_degrees(gps_data["GPSLatitude"])
        lon = convert_to_degrees(gps_data["GPSLongitude"])

        if gps_data.get("GPSLatitudeRef") == "S":
            lat = -lat
        if gps_data.get("GPSLongitudeRef") == "W":
            lon = -lon

        print("Converted Lat:", lat)
        print("Converted Lon:", lon)

        if lat is None or lon is None:
            print("Skipping due to conversion issue")
            continue

        predictions = detect_landmark(image_path)
        cnn_prediction = predictions[0][0]

        city, state, country = get_location_name(lat, lon)

        final_landmark = infer_landmark(city, cnn_prediction)

        insert_data(lat, lon, timestamp, final_landmark)

        print(f"Processed: {image_name}")

generate_map()
generate_report()