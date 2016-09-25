"""Test models of Comics app."""

from django.test import TestCase
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher


# ------------------------------------------------------------------ #
#
#                         Auxiliar Functions
#
# ------------------------------------------------------------------ #
def create_artist(name='Test Artist', nationality='ES'):
        """Create an Artist external function."""
        bio = 'This is a test biography for Mr <{}>'.format(name)
        return Artist.objects.create(name=name,
                                     nationality=nationality,
                                     biography=bio)


def create_publisher(name='Test Publisher', nationality='ES'):
        """Create a Publisher external function."""
        history = 'This is a test history for <{}>'.format(name)
        return Publisher.objects.create(name=name,
                                        nationality=nationality,
                                        history=history)


def create_colection(name='Test Colection', subname='extra subname',
                     vol=1, language='ES', distributor_id='1',
                     colection_type='Regular', max_numbers=12):
        """Create a Colection external function."""
        return Colection.objects.create(name=name,
                                        subname=subname,
                                        volume=vol,
                                        language=language,
                                        max_numbers=max_numbers,
                                        colection_type=colection_type,
                                        distributor=distributor_id,
                                        )


# ------------------------------------------------------------------ #
#
#                            Artist Tests
#
# ------------------------------------------------------------------ #
class ArtistTest(TestCase):
    """Artist class tests."""

    def test_artist_creation(self):
        """Unitest for Artists creation.

        Sample output:
        Artist 1: <Frank Miller> from <United States of America>
        Artist 2: <Salvador Larroca> from <Spain>
        """
        a1 = create_artist('Frank Miller', 'US')
        a2 = create_artist('Salvador Larroca', 'ES')

        self.assertTrue(isinstance(a1, Artist))
        self.assertTrue(isinstance(a2, Artist))
        self.assertEqual(a1.nationality.name, 'United States of America')
        self.assertEqual(a2.nationality.name, 'Spain')


# ------------------------------------------------------------------ #
#
#                            Colection Tests
#
# ------------------------------------------------------------------ #
class ColectionTest(TestCase):
    """Colection class tests."""

    def test_colection_creation(self):
        """Test for creating an object from model Colection."""
        p1 = create_publisher(name='TestPublisher002', nationality='ES')
        c1 = create_colection(
            name='Xmen', subname='children of the atom', vol=2,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=50)

        self.assertTrue(isinstance(c1, Colection))
        self.assertEqual(c1.language.name, 'Spain')


# ------------------------------------------------------------------ #
#
#                            Publisher Tests
#
# ------------------------------------------------------------------ #
class PublisherTest(TestCase):
    """Publisher class tests."""

    def test_publisher_creation(self):
        """Test for creating an object from model Publisher."""
        p1 = create_publisher(name='Marvel', nationality='US')
        p2 = create_publisher(name='Forum', nationality='ES')

        self.assertTrue(isinstance(p1, Publisher))
        self.assertTrue(isinstance(p2, Publisher))
        self.assertEqual(p1.nationality.name, 'United States of America')
        self.assertEqual(p2.nationality.name, 'Spain')
