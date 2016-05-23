"""Test models of Comics app."""

from django.test import TestCase
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher


class ArtistTest(TestCase):
    """Artist class tests."""

    def create_artist(self, name='Test Artist', nationality='ES'):
        """Internal method to create an artist model."""
        bio = 'This is a test biography for Mr <{}>'.format(name)
        return Artist.objects.create(name=name, nationality=nationality,
                                     biography=bio)

    def test_artist_creation(self):
        """Unitest for Artists creation.

        Sample output:
        Artist 1: <Frank Miller> from <United States of America>
        Artist 2: <Salvador Larroca> from <Spain>
        """
        a1 = self.create_artist('Frank Miller', 'US')
        a2 = self.create_artist('Salvador Larroca', 'ES')

        print
        print "Artists creation tests . . ."
        print
        print "Artist 1: <{}> from <{}>".format(a1.name, a1.nationality.name)
        print "     Bio: {}".format(a1.biography)
        print "Artist 2: <{}> from <{}>".format(a2.name, a2.nationality.name)
        print "     Bio: {}".format(a2.biography)

        self.assertTrue(isinstance(a1, Artist))
        self.assertTrue(isinstance(a2, Artist))
        self.assertEqual(a1.nationality.name, 'United States of America')
        self.assertEqual(a2.nationality.name, 'Spain')


class ColectionTest(TestCase):
    """Colection class tests."""

    def create_colection(self, name='Test Colection', subname='extra subname',
                         vol=1, maxnumbers=12, numbers=12):
        """Internal method to create a colection model."""
        return Colection.objects.create(name=name, subname=subname, volume=vol,
                                        max_numbers=maxnumbers,
                                        numbers=numbers)

    def test_colection_creation(self):
        """Test for creating an object from model Colection."""
        c1 = self.create_colection('Xmen', 'children of the atom', 2, 50, 30)
        c2 = self.create_colection('Alpha Flight', 'canada heroes', 1, 60, 50)

        print
        print "Colection creation tests . . ."
        print
        self.assertTrue(isinstance(c1, Colection))
        self.assertTrue(isinstance(c2, Colection))
        # self.assertEqual(a1.nationality.name, 'United States of America')
        # self.assertEqual(a2.nationality.name, 'Spain')


class PublisherTest(TestCase):
    """Publisher class tests."""

    def create_publisher(self, name='Test Publisher', history='My test story'):
        """Internal method to create a colection model."""
        return Publisher.objects.create(name=name, history=history)

    def test_publisher_creation(self):
        """Test for creating an object from model Publisher."""
        p1 = self.create_publisher('Marvel', 'the big factory')
        p2 = self.create_publisher('DC', 'second on flight')

        print
        print "Publisher creation tests . . ."
        print
        self.assertTrue(isinstance(p1, Publisher))
        self.assertTrue(isinstance(p2, Publisher))
