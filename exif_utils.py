from struct import error as StructError

import piexif


def _reference(ref):
    if isinstance(ref, bytes):
        ref = ref.decode('ascii', errors='ignore')
    return ref.upper() if isinstance(ref, str) else None


def get_gps(image_bytes: bytes) -> tuple[float, float] | None:
    try:
        gps = piexif.load(image_bytes).get("GPS", {})
        lat = _to_degrees(gps[piexif.GPSIFD.GPSLatitude])
        lon = _to_degrees(gps[piexif.GPSIFD.GPSLongitude])
        lat_ref = _reference(gps.get(piexif.GPSIFD.GPSLatitudeRef))
        lon_ref = _reference(gps.get(piexif.GPSIFD.GPSLongitudeRef))
    except (KeyError, ValueError, TypeError, OSError, IndexError, ZeroDivisionError, StructError):
        return None

    if lat_ref not in {"N", "S"} or lon_ref not in {"E", "W"}:
        return None
    if not (0 <= lat <= 90 and 0 <= lon <= 180):
        return None
    return (-lat if lat_ref == "S" else lat, -lon if lon_ref == "W" else lon)

def _to_degrees(value):
    d, m, s = value
    return d[0]/d[1] + (m[0]/m[1])/60 + (s[0]/s[1])/3600
