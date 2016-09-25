"""Test views of Comics app."""

from django.test import TestCase
from django.conf import settings as mysettings

from comics.tests.common import create_artist
from comics.tests.common import create_publisher
from comics.tests.common import create_colection
# from comics.tests.common import create_comic

proj_name = mysettings.PROJECT_NAME


# ------------------------------------------------------------------ #
#
#                            Artist Tests
#
# ------------------------------------------------------------------ #
class ArtistViewsTest(TestCase):
    """Artist Views class tests."""

    def test_artist_view(self):
        """Test for checking publisher views."""
        a1 = create_artist('Frank Miller', 'US')
        a1_url = '/{}/artists/{}/'.format(proj_name, a1.slug)
        response = self.client.get(a1_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='comics/artist.html')


# ------------------------------------------------------------------ #
#
#                            Publisher Tests
#
# ------------------------------------------------------------------ #
class PublisherViewsTest(TestCase):
    """Publisher Views class tests."""

    def test_publisher_view(self):
        """Test for checking publisher views."""
        p1 = create_publisher(name='DC Comics', nationality='US')
        p1_url = '/{}/publishers/{}/'.format(proj_name, p1.slug)
        response = self.client.get(p1_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='comics/publisher.html')


# ------------------------------------------------------------------ #
#
#                            Colection Tests
#
# ------------------------------------------------------------------ #
class ColectionViewsTest(TestCase):
    """Colection Views class tests."""

    def test_colection_view(self):
        """Test for checking publisher views."""
        p1 = create_publisher(name='TestPublisher009', nationality='ES')
        c1 = create_colection(
            name='The Amazing Spiderman', subname='Peter Parker is...', vol=1,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=50)
        c1_url = '/{}/colections/{}/'.format(proj_name, c1.slug)
        response = self.client.get(c1_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='comics/colection.html')


# ------------------------------------------------------------------ #
#
#                            Comic Tests
#
# ------------------------------------------------------------------ #
class ComicViewsTest(TestCase):
    """Comic Views class tests."""

    def test_comic_view(self):
        """."""
        pass
