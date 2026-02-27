from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    gps_data = {}
    timestamp = None

    if exif_data:
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)

            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

            if decoded == "DateTime":
                timestamp = value

    return gps_data, timestamp


def convert_to_degrees(value):
    try:
        # Handle float-style GPS (like your phone image)
        if isinstance(value[0], float) or hasattr(value[0], 'numerator'):
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
        else:
            # Handle tuple style GPS
            d = value[0][0] / value[0][1]
            m = value[1][0] / value[1][1]
            s = value[2][0] / value[2][1]

        return d + (m / 60.0) + (s / 3600.0)

    except Exception as e:
        print("GPS conversion error:", e)
        return None