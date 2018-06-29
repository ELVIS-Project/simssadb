from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.models.custom_base_model import CustomBaseModel
from database.models.genre import Genre
from database.models.section import Section


class MusicalWork(CustomBaseModel):
    """
    A complete work of music

    A purely abstract entity that can manifest in differing versions.
    Divided into sections.
    Must have at least one section.
    """
    variant_titles = ArrayField(
                    models.CharField(max_length=200, blank=True),
                    blank=False, null=False, default=['hello', 'world'],
                    help_text='All the titles commonly attributed to this '
                              'Musical Work. Include the opus number '
                              'if there is one')

    genres_as_in_style = models.ManyToManyField(Genre,
                                                related_name='style',
                                                help_text='The styles '
                                                          'attributed to this '
                                                          'Musical Work, '
                                                          'i.e. Classical, '
                                                          'Pop, Folk')
    genres_as_in_form = models.ManyToManyField(Genre,
                                               related_name='form',
                                               help_text='The forms '
                                                         'attributed to this '
                                                         'Musical Work, '
                                                         'i.e. Sonata, Motet, '
                                                         '12-bar Blues')

    sections = models.ManyToManyField(Section, related_name='in_works',
                                      help_text='The Sections that this work '
                                                'contains. If the Musical '
                                                'Work is not formally divided '
                                                'into Sections, then it has '
                                                'one Section.')
    religiosity = models.NullBooleanField(null=True, blank=True, default=None,
                                          help_text='Whether the Musical Work is'
                                                    ' secular or religious. '
                                                    'Leave this blank if non '
                                                    'applicable.')
    authority_control_url = models.URLField(null=True, blank=True,
                                            help_text='An URI linking to an '
                                                      'authority control '
                                                      'description of this '
                                                      'Musical Work')
    authority_control_key = models.IntegerField(unique=True, blank=True,
                                                null=True,
                                                help_text='The identifier of '
                                                          'this Musical Work '
                                                          'in the authority '
                                                          'control')
    contributors = models.ManyToManyField(
                                        'Person',
                                        through='ContributedTo',
                                        through_fields=(
                                            'contributed_to_work', 'person'),
                                        help_text='All the People that '
                                                  'contributed to this '
                                                  'Musical Work in different '
                                                  'capacities such as '
                                                  'composer or arranger')

    @property
    def composers(self):
        """
        Gets a list of the contribution to this Work by composers

        :returns a list of dictionaries
        Each dictionary contains the composer, the date, the location and
        the certainty of the contribution
        """
        composers_info = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            info = {'composer': relationship.person,
                    'date':     relationship.date,
                    'location': relationship.location,
                    'certain':  relationship.certain}
            composers_info.append(info)
        return composers_info

    @property
    def symbolic_files(self):
        """Gets all the Symbolic Files related to this Work"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.append(source.manifested_by_sym_file.all())
        return files

    @property
    def symbolic_music_formats(self):
        """Gets the formats of all the Symbolic Files related to this Work"""
        formats = set()
        files = self.symbolic_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def image_files(self):
        """Gets all the Image Files related to this Work"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.append(source.manifested_by_image_file.all())
        return files


    @property
    def image_formats(self):
        """Gets the formats of all the Image Files related to this Work"""
        formats = set()
        files = self.image_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def dates_of_composition(self):
        """Gets the date of contribution of all the composers of this Work"""
        dates = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            dates.append(relationship.date)
        return dates

    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work"""
        places = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            places.append(relationship.location)
        return places

    @property
    def parts(self):
        """Gets all the Parts related to this Musical Work"""
        parts = []
        for section in self.sections.all():
            parts.extend(section.parts.all())
        return parts

    @property
    def instrumentation(self):
        """Gets all the Instruments used in this Musical Work"""
        instruments = set()
        for part in self.parts:
            instruments.add(part.written_for)
        return instruments

    @property
    def features(self):
        """Gets all the Features extracted from files related to this Work"""
        features = []
        sym_files = self.symbolic_files
        for file in sym_files:
            for feature in file.extractedfeature_set.all():
                features.append(feature)
        return features

    @property
    def collections_of_sources(self):
        """Gets all the Collections of Sources related to this Work"""
        collections = set()
        sources = self.sources.all()
        for source in sources:
            collections.add(source.part_of_collection)
        return collections

    @property
    def languages(self):
        """Gets all the languages of the Sources and Text Files related to this Work"""
        languages = set()
        sources = self.sources.all()
        # This is a bit ugly, but I'm not sure how to do it better
        for source in sources:
            for language in source.languages:
                languages.add(language)
            for text_file in source.manifested_by_Text_file.all():
                for language in text_file.languages:
                    languages.add(language)
        return languages

    @property
    def certainty(self):
        """Returns True if all the relationships have certain == True"""
        for relationship in self.contributed_to.all():
            if not relationship.certain:
                return False
        return True

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
