"""Test views of Comics app."""

from django.test import TestCase

from django.template.defaultfilters import slugify
from django.conf import settings as mysettings
from comics.models import Publisher

proj_name = mysettings.PROJECT_NAME


class PublisherViewsTest(TestCase):
    """Publisher Views class tests."""

    def test_publisher_view(self):
            """Test for checking publisher views."""
            publisher_name = "Marvel Comics"
            publisher_name_slug = slugify(publisher_name)
            publisher_story = "my publisher story"
            p1 = Publisher.objects.create(name=publisher_name,
                                          history=publisher_story)

            p1_url = '/{}/publishers/{}/'.format(proj_name,
                                                 publisher_name_slug)
            response = self.client.get(p1_url)

            print
            print "Publisher view tests . . ."
            print "    getting <{}> view page . . .".format(p1)
            print "    checking {}".format(p1_url)
            print "    response: {}".format(response.status_code)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response,
                                    template_name='comics/publisher.html')
