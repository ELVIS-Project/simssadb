from django.contrib.postgres.fields import ArrayField
from django.db import models

from database.models.collection_of_sources import CollectionOfSources
from database.models.custom_base_model import CustomBaseModel
from database.models.musical_work import MusicalWork
from database.models.part import Part
from database.models.section import Section


class Source(CustomBaseModel):
    """
    Represents a document containing the music defining a Work/Section/Part

    Must be part of a Collection of Sources.
    """
    languages = ArrayField(models.CharField(max_length=200, blank=True),
                           blank=True, null=True,
                           help_text='The languages this Source is written in')
    work = models.ForeignKey(MusicalWork, null=False, blank=False,
                             on_delete=models.PROTECT,
                             help_text='The Musical Work manifested in part '
                                       'or in full by this Source',
                             default=0,
                             related_name='sources')
    sections = models.ManyToManyField(Section,
                                      help_text='The Section or Sections '
                                                'manifested in full by this '
                                                'Source')
    parts = models.ManyToManyField(Part,
                                   help_text='The Part or Parts '
                                             'manifested in full by this '
                                             'Source')
    part_of_collection = models.ForeignKey(CollectionOfSources, null=False,
                                           blank=False,
                                           on_delete=models.PROTECT,
                                           help_text='The Collection of '
                                                     'Sources this Source '
                                                     'belongs to')
    parent_sources = models.ManyToManyField('self',
                                            related_name='child_sources',
                                            blank=True,
                                            help_text='The Source this Source '
                                                      'derives from')
    portion = models.TextField(max_length=255, blank=True, null=True,
                               help_text='Specifies which portion of the '
                                         'Collection of Sources this Source '
                                         'represents. i.e. a page range, '
                                         'a number of folios, a number of '
                                         'files in a database, etc')
    url = models.URLField(null=True, blank=True,
                          help_text='An link back to an electronic version of '
                                    'this Source, if it exists')

    def __str__(self):
        return "Part of {0}, source of ".format(self.part_of_collection.title,
                                                self.work.variant_titles[0])


    @property
    def encoders(self):
        """Gets all the Encoders of files that manifest this Source"""
        encoders = set()
        for sym_file in self.manifested_by_sym_files:
            encoders.add(sym_file.encoded_with)
        for text_file in self.manifested_by_text_files:
            encoders.add(text_file.encoded_with)
        for audio_file in self.manifested_by_audio_files:
            encoders.add(audio_file.encoded_with)
        for image_file in self.manifested_by_image_files:
            encoders.add(image_file.encoded_with)
        return encoders

    class Meta(CustomBaseModel.Meta):
        db_table = 'source'
