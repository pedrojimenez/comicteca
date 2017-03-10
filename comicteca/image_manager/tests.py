# Create your tests here.
"""Test models of ImageManager app."""

from django.test import TestCase
from image_manager.models import ImageManager


# ------------------------------------------------------------------ #
#
#                           ImageManager Tests
#
# ------------------------------------------------------------------ #
class ImageManagerTest(TestCase):
    """ImageManager class tests."""
    extensions = ['jpg', 'jpeg', 'png']
    test_urls = ['https://www.python.org/static/img/python-logo.jpg',
                 'https://www.python.org/static/img/python-logo.jpeg',
                 'https://www.python.org/static/img/python-logo.png',
                 'https://www.python.org/',
                 ]

    def test_valid_extensions_property(self):
        """
        Test for ImageManager property "valid_extensions".
        """
        m = ImageManager()
        self.assertEqual(self.extensions, m.valid_extensions)

    def test_is_valid_extension_method(self):
        """
        Test for ImageManager "is_valid_extension" method.
        """
        m = ImageManager()
        self.assertEqual(True, m.is_valid_image_extension(self.test_urls[0]))
        self.assertEqual(True, m.is_valid_image_extension(self.test_urls[1]))
        self.assertEqual(True, m.is_valid_image_extension(self.test_urls[2]))
        self.assertEqual(False, m.is_valid_image_extension(self.test_urls[3]))

    def test_check_http_url_method(self):
        """
        Test for ImageManager "check_http_url" method.
        """
        m = ImageManager()
        self.assertEqual(None, m.check_http_url(self.test_urls[0]))
        self.assertEqual(None, m.check_http_url(self.test_urls[1]))
        self.assertEqual(200, m.check_http_url(self.test_urls[2]).code)

    def test_get_extension_from_url_image_method(self):
        """
        Test for ImageManager "get_extension_from_url_image" method.
        """
        m = ImageManager()
        self.assertEqual('jpg', m.get_extension_from_url_image(self.test_urls[0]))
        self.assertEqual('jpeg', m.get_extension_from_url_image(self.test_urls[1]))
        self.assertEqual('png', m.get_extension_from_url_image(self.test_urls[2]))
        self.assertEqual('org/', m.get_extension_from_url_image(self.test_urls[3]))

