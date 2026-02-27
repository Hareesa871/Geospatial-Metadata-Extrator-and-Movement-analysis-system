from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geo_tracker")

def get_location_name(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), timeout=10)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village')
            state = address.get('state')
            country = address.get('country')
            return city, state, country
    except:
        pass

    return None, None, None