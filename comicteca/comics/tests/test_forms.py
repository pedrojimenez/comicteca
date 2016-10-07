"""Test views of Comics app."""
from django.test import TestCase
from django.template.defaultfilters import slugify
from django.conf import settings as mysettings
from comics.tests.common import create_publisher

proj_name = mysettings.PROJECT_NAME
HTTP_OK_CODE = 200


# ------------------------------------------------------------------ #
#
#                            Artist Tests
#
# ------------------------------------------------------------------ #
class ArtistFormsTest(TestCase):
    """Artist Forms class tests."""

    def test_artist_form(self):
        """Test for checking artist form.

        It will insert one Artist from the PublisherForm
        and check if is accesible via its direct url.
        """
        artist_name = "Stan Lee"
        artist_country = "US"
        artist_story = "The artist great story"
        artist_name_slug = slugify(artist_name)
        form_url = '/{}/add_artist/'.format(proj_name)
        p1_url = '/{}/artists/{}/'.format(proj_name,
                                          artist_name_slug)
        response = self.client.post(form_url, {'name': artist_name,
                                               'nationality': artist_country,
                                               'history': artist_story})
        response_view = self.client.get(p1_url)
        self.assertEqual(response.status_code, HTTP_OK_CODE)
        self.assertEqual(response_view.status_code, HTTP_OK_CODE)


# ------------------------------------------------------------------ #
#
#                            Publisher Tests
#
# ------------------------------------------------------------------ #
class PublisherFormsTest(TestCase):
    """Publisher Forms class tests."""

    def test_publisher_form(self):
        """Test for checking publisher form.

        It will insert one Publisher from the PublisherForm
        and check if is accesible via its direct url.
        """
        pub_name = "Panini Comics"
        pub_country = "ES"
        pub_story = "my publisher story"
        pub_name_slug = slugify(pub_name)
        form_url = '/{}/add_publisher/'.format(proj_name)
        p1_url = '/{}/publishers/{}/'.format(proj_name,
                                             pub_name_slug)
        response = self.client.post(form_url, {'name': pub_name,
                                               'nationality': pub_country,
                                               'history': pub_story})
        response_view = self.client.get(p1_url)
        # print
        # print "Publisher form tests . . ."
        # print "    Inserting <{}> from form page...".format(pub_name)
        # print "    checking {}".format(form_url)
        # print "    response: {}".format(response.status_code)
        # print "    checking {}".format(p1_url)
        # print "    response: {}".format(response_view.status_code)
        self.assertEqual(response.status_code, HTTP_OK_CODE)
        self.assertEqual(response_view.status_code, HTTP_OK_CODE)


# ------------------------------------------------------------------ #
#
#                            Colection Tests
#
# ------------------------------------------------------------------ #
class ColectionFormsTest(TestCase):
    """Colection Forms class tests."""

    def test_colection_form(self):
        """Test for checking colection form.

        It will insert one Colection from the ColectionForm
        and check if is accesible via its direct url.
        """
        distributor = create_publisher(name='Forum', nationality='US')
        editor1 = create_publisher(name='Marvel', nationality='US')

        name = "The incredible Hulk"
        subname = "Green Stories"
        volume = 1
        language = "ES"
        max_numbers = 12
        colection_type = 'regular'
        colection_slug = slugify(name)

        form_url = '/{}/colections/add/'.format(proj_name)
        p1_url = '/{}/colections/{}/'.format(proj_name,
                                             colection_slug)

        response = self.client.post(
            form_url, {'name': name,
                       'subname': subname,
                       'volume': volume,
                       'language': language,
                       'max_numbers': max_numbers,
                       'colection_type': colection_type,
                       'distributor': distributor,
                       'editors': editor1,
                       })
        response_view = self.client.get(p1_url)
        self.assertEqual(response.status_code, HTTP_OK_CODE)
        self.assertEqual(response_view.status_code, HTTP_OK_CODE)


# ------------------------------------------------------------------ #
#
#                            Comic Tests
#
# ------------------------------------------------------------------ #
class ComicFormsTest(TestCase):
    """Comic Forms class tests."""

    def test_comic_form(self):
        """Test for checking comic form.

        It will insert one Comic from the ComicForm
        and check if is accesible via its direct url.
        """
        pass
