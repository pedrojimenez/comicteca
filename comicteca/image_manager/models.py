from django.db import models


# Create your models here.
class ImageManager(models.Model):
    """Class for managing all image operations."""

    __valid_extensions = ['jpg', 'jpeg', 'png']

    @property
    def valid_extensions(self):
        """Return the list of supported/valid image extensions."""
        return self.__valid_extensions

    def is_valid_image_extension(self, url):
        """Check if input url is a valid image."""
        if not url:
            msg = 'The given URL is empty'
            # TODO: logger.error(msg)
            print msg
            return False

        extension = self.get_extension_from_url_image(url)

        return extension in self.valid_extensions

    def check_http_url(self, url):
        """Check if current url is accesible and return the http response."""
        import urllib2
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request)
            msg = "({}) image url is correct: {}".format(
                response.getcode(), url)
            # TODO: logger.info(msg)
            print msg
            return response
        except urllib2.HTTPError as e:  # 404, 500, etc..
            msg = "ERROR ({}) getting the image from the url: {}".format(
                e, url)
            # TODO: logger.error(msg)
            print msg
            return None

    def get_extension_from_url_image(self, url):
        """Get the last part of the url and check against."""
        if not url:
            return None
        return url.rsplit('.', 1)[1].lower()
