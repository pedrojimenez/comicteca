"""Test views of Comics app."""

from django.test import TestCase

from django.template.defaultfilters import slugify
from django.conf import settings as mysettings
from comics.models import Publisher
from comics.models import Colection
from comics.models import Artist

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


class ColectionViewsTest(TestCase):
    """Publisher Views class tests."""

    def test_colection_view(self):
            """Test for checking publisher views."""
            colection_name = "The amazing Spiderman"
            colection_name_slug = slugify(colection_name)
            c1 = Colection.objects.create(name=colection_name)
            c1_url = '/{}/colections/{}/'.format(proj_name,
                                                 colection_name_slug)
            response = self.client.get(c1_url)

            print
            print "Colection view tests . . ."
            print "    getting <{}> view page . . .".format(c1)
            print "    checking {}".format(c1_url)
            print "    response: {}".format(response.status_code)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response,
                                    template_name='comics/colection.html')


class ArtistViewsTest(TestCase):
    """Artist Views class tests."""

    def test_artist_view(self):
            """Test for checking publisher views."""
            artist_name = "Stan Lee"
            artist_nationality = "US"
            artist_name_slug = slugify(artist_name)
            a1 = Artist.objects.create(name=artist_name,
                                       nationality=artist_nationality)
            a1_url = '/{}/artists/{}/'.format(proj_name,
                                              artist_name_slug)
            response = self.client.get(a1_url)

            print
            print "Artist view tests . . ."
            print "    getting <{}> view page . . .".format(a1)
            print "    checking {}".format(a1_url)
            print "    response: {}".format(response.status_code)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response,
                                    template_name='comics/artist.html')
