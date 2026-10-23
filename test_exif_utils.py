import io
import unittest

import piexif
from PIL import Image

from exif_utils import get_gps_or_mock


def make_image(latitude_ref, longitude_ref):
    gps = {
        piexif.GPSIFD.GPSLatitudeRef: latitude_ref,
        piexif.GPSIFD.GPSLongitudeRef: longitude_ref,
        piexif.GPSIFD.GPSLatitude: ((33, 1), (30, 1), (0, 1)),
        piexif.GPSIFD.GPSLongitude: ((70, 1), (40, 1), (0, 1)),
    }
    image = io.BytesIO()
    Image.new('RGB', (2, 2)).save(image, format='JPEG', exif=piexif.dump({'GPS': gps}))
    return image.getvalue()


class GpsReferenceTests(unittest.TestCase):
    def test_south_west_coordinates_are_negative_for_byte_and_string_refs(self):
        for south, west in ((b'S', b'W'), ('S', 'W')):
            with self.subTest(latitude_ref=south, longitude_ref=west):
                latitude, longitude = get_gps_or_mock(make_image(south, west))
                self.assertAlmostEqual(latitude, -33.5)
                self.assertAlmostEqual(longitude, -70 - 40 / 60)

    def test_north_east_coordinates_remain_positive(self):
        latitude, longitude = get_gps_or_mock(make_image(b'N', b'E'))
        self.assertGreater(latitude, 0)
        self.assertGreater(longitude, 0)


if __name__ == '__main__':
    unittest.main()
