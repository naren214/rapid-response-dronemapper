import piexif, random

MOCK_LAT_RANGE = (12.90, 12.95)
MOCK_LON_RANGE = (80.10, 80.20)

def get_gps_or_mock(image_bytes: bytes) -> tuple:
    try:
        exif_dict = piexif.load(image_bytes)
        gps = exif_dict.get("GPS", {})
        if gps:
            lat = _to_degrees(gps[piexif.GPSIFD.GPSLatitude])
            lon = _to_degrees(gps[piexif.GPSIFD.GPSLongitude])
            return lat, lon
    except Exception:
        pass
    return random.uniform(*MOCK_LAT_RANGE), random.uniform(*MOCK_LON_RANGE)

def _to_degrees(value):
    d, m, s = value
    return d[0]/d[1] + (m[0]/m[1])/60 + (s[0]/s[1])/3600