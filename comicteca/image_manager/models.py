from django.db import models


# Create your models here.
class ImageManager(models.Model):
    """Class for managing all image operations."""

    __valid_extensions = ['jpg', 'jpeg', 'png']

    def is_valid_image_extension(self, url):
        """Check if input url is a valid image."""
        if not url:
            msg = 'The given URL is empty'
            print msg
            return 1

        # Get the last part of the url and check against
        extension = url.rsplit('.', 1)[1].lower()

        if extension not in self.__valid_extensions:
            msg = 'The given URL does not match valid image extensions.'
            print msg
            return 1

        return 0
