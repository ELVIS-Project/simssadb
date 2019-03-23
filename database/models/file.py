"""Define a File model"""
from typing import List

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import QuerySet

from database.models.custom_base_model import CustomBaseModel


class File(CustomBaseModel):
    """Base abstract model with fields common to all file types.

    Most if not all fields should be extracted automatically
    
    Attributes
    ----------
    File.file_type : models.CharField
        The format of this File

    File.file_size : models.PositiveIntegerField
        The size of the this File in bytes

    File.version : models.CharField
        The version of the encoding schema of this File

    File.encoding_date : models.DateTimeField
        The date this File was encoded

    File.encoded_with : models.ForeignKey
        A reference to the Encoder of this File

    File.validated_by : models.ForeignKey
        A reference to the Validator of this File

    File.extra_metadata : django.contrib.postgres.fields.JSONField
        Any extra metadata associated with this File

    File.manifests : None
        Subclasses must override

    File.file : models.FileField
        The path to the actual file stored on disk
    """
    file_type = models.CharField(max_length=100,
                                 help_text='The format of the '
                                           'File')
    file_size = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            help_text='The size of the File '
                                                      'in bytes')
    version = models.CharField(max_length=20,
                               null=True,
                               blank=True,
                               help_text='The version of the encoding schema '
                                         '(i.e. MEI 2.0)')
    encoding_date = models.DateTimeField(null=True,
                                         help_text='The date the File was '
                                                   'encoded')
    encoded_with = models.ForeignKey('Encoder',
                                     on_delete=models.PROTECT,
                                     null=True,
                                     blank=True,
                                     help_text='The Encoder of '
                                               'this File')
    validated_by = models.ForeignKey('Validator',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     help_text='The Validator of this file')
    extra_metadata = JSONField(null=True,
                               blank=True,
                               help_text='Any extra metadata associated with '
                                         'the File')
    manifests = None  # Must override in classes that inherit from this!

    class Meta(CustomBaseModel.Meta):
        abstract = True

    @property
    def source(self):
        """Return the Source of this File

        Returns
        -------
        Source
            The Source of this File
        """
        return self.manifests.source

    @property
    def musical_work(self):
        """Return the MusicalWork the Source of this File is
        related to

        Returns
        -------
        MusicalWork
            The MusicalWork the Source of this File is related to
        """
        if self.manifests.work:
            return self.manifests.work
        elif self.manifests.sections.first():
            return self.manifests.sections.first().musical_work
        else:
            return self.manifests.parts.first().section.musical_work

    @property
    def sections(self) -> QuerySet:
        """Return the Sections manifested in full by the Source
        of this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Sections the Source of this
            File is related to
        """
        return self.manifests.sections.all()

    @property
    def parts(self) -> QuerySet:
        """Return the Parts manifested in full by the Source of
        this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Parts the Source of this File
            is related to
        """
        return self.manifests.parts.all()

    @property
    def composers(self) -> QuerySet:
        """Return the composers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the composers
        """
        return self.musical_work.composers

    @property
    def sacred_or_secular(self) -> str:
        """Return the _sacred_or_secular of the MusicalWork related to this file

        Returns
        -------
        str
            The _sacred_or_secular of the MusicalWork related to this file
        """
        return self.musical_work.sacred_or_secular

    @property
    def certainty(self) -> bool:
        """Return the certainty of the MusicalWork related to this File

        Returns
        -------
        bool
            The certainty of attribution of the MusicalWork related to this File
        """
        return self.musical_work.certainty_of_attributions

    @property
    def genres_as_in_type(self) -> QuerySet:
        """Return the Genres (type) of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            The Genres (type) of the MusicalWork related to this File
        """
        return self.musical_work.genres_as_in_type.all()

    @property
    def genres_as_in_style(self) -> QuerySet:
        """Return the Genres (style) of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            The Genres (style) of the MusicalWork related to this File
        """
        return self.musical_work.genres_as_in_style.all()

    @property
    def composers_dates(self) -> List[str]:
        """Return the dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of composition
        """
        return self.musical_work.composers_dates

    @property
    def composers_locations(self) -> QuerySet:
        """Return the places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was composed
        """
        return self.musical_work.composers_locations

    @property
    def instrumentation(self) -> QuerySet:
        """Return the Instruments of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Instruments of the MusicalWork related to this
            File
        """
        return self.musical_work.instrumentation
