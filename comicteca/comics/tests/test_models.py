"""Test models of Comics app."""

from django.test import TestCase
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic

from comics.tests.common import create_artist
from comics.tests.common import create_publisher
from comics.tests.common import create_colection
from comics.tests.common import create_comic
from comics.tests.common import create_user


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

    def test_colection_missing_comics(self):
        """
        Test for returning missing comics from a collection.

        A collection can begin in a specific number and have max_numbers
        So it could be:
          - from 0..7 (8 numbers)
          - from 1..12 (12 numbers)
          - from 12..38 (26 numbers)
        """
        u1 = create_user(username='User001')
        p1 = create_publisher(name='TestPublisher003', nationality='ES')

        c1 = create_colection(
            name='Superman', subname='The man of Steel', vol=2,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=8, initial_number=0)

        c2 = create_colection(
            name='Flash', subname='Hyper speed', vol=1,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=12, initial_number=1)

        c3 = create_colection(
            name='Wonder Woman', subname='Amazing', vol=1,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=26, initial_number=12)

        c1.complete_colection(user=u1)
        c2.complete_colection(user=u1)
        c3.complete_colection(user=u1)

        missing_list_c1 = c1.get_missing_comics()
        missing_list_c2 = c2.get_missing_comics()
        missing_list_c3 = c3.get_missing_comics()

        self.assertEqual(len(missing_list_c1), 0)
        self.assertEqual(len(missing_list_c2), 0)
        self.assertEqual(len(missing_list_c3), 0)


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


# ------------------------------------------------------------------ #
#
#                            Comic Tests
#
# ------------------------------------------------------------------ #
class ComicTest(TestCase):
    """Comic class tests."""

    def test_comic_creation(self):
        """Test for creating an object from model Comic."""
        p1 = create_publisher(name='TestPublisher002', nationality='US')
        c1 = create_colection(
            name='Xmen2', subname='children of the atom', vol=2,
            language='ES', distributor_id=p1, colection_type='Regular',
            max_numbers=50)
        comic = create_comic(title='Return of Colossus', number=10, pages=64,
                             collection=c1)

        self.assertTrue(isinstance(p1, Publisher))
        self.assertTrue(isinstance(c1, Colection))
        self.assertTrue(isinstance(comic, Comic))
        self.assertEqual(p1.nationality.name, 'United States of America')
        self.assertEqual(c1.language.name, 'Spain')
        self.assertEqual(c1.numbers, 1)
