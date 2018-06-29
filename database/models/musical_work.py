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
        """Gets a list of the contributors to this piece that are composers"""
        composers = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            composers.append(relationship.person)
        return composers


    @property
    def symbolic_files(self):
        files = []
        sources = self.sources.all()
        for source in sources:
            files.append(source.manifested_by_sym_file.all())
        return files

    @property
    def symbolic_music_formats(self):
        """Gets the formats of all the Symbolic Files related to this Work"""
        formats = set(())
        files = self.symbolic_files
        for file in files:
            formats.add(file.file_type)
        return formats

    def __str__(self):
        return "{0}".format(self.variant_titles[0])

    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_work'
