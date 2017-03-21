"""Common/auxiliary functions for all tests."""
from comics.models import Artist
from comics.models import Colection
from comics.models import Publisher
from comics.models import Comic
from django.contrib.auth.models import User


# ------------------------------------------------------------------ #
#
#                      Creation Auxiliar Functions
#
# ------------------------------------------------------------------ #
def create_user(username='TestUser'):
    """Create an Artist external function."""
    return User.objects.create(username=username)


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
                     vol=1, language='ES', distributor_id=1,
                     colection_type='Regular', max_numbers=12,
                     initial_number=1):
    """Create a Colection external function."""
    return Colection.objects.create(name=name,
                                    subname=subname,
                                    volume=vol,
                                    language=language,
                                    initial_number=initial_number,
                                    max_numbers=max_numbers,
                                    colection_type=colection_type,
                                    distributor=distributor_id,
                                    )


def create_comic(collection, title='Test Comic Title', number=1, pages=24):
        """Create a Comic external function."""
        return Comic.objects.create(title=title,
                                    number=number,
                                    pages=pages,
                                    colection=collection,
                                    )
