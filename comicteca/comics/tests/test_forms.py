"""Test views of Comics app."""

from django.test import TestCase

from django.template.defaultfilters import slugify
from django.conf import settings as mysettings
# from comics.models import Publisher
# from comics.models import Colection
# from comics.models import Artist

proj_name = mysettings.PROJECT_NAME


class PublisherFormsTest(TestCase):
    """Publisher Forms class tests."""

    def test_publisher_form(self):
            """Test for checking publisher form."""
            publisher_name = "Panini Comics"
            publisher_story = "my publisher story"
            publisher_name_slug = slugify(publisher_name)

            form_url = '/{}/add_publisher/'.format(proj_name)
            p1_url = '/{}/publishers/{}/'.format(proj_name,
                                                 publisher_name_slug)

            response = self.client.post(form_url, {'name': publisher_name,
                                                   'history': publisher_story})

            response_view = self.client.get(p1_url)

            print
            print "Publisher form tests . . ."
            print "    Inserting <{}> from form page...".format(publisher_name)
            print "    checking {}".format(form_url)
            print "    response: {}".format(response.status_code)
            print "    checking {}".format(p1_url)
            print "    response: {}".format(response_view.status_code)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_view.status_code, 200)
