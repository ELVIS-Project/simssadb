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

    file_type = models.CharField(max_length=100, help_text="The format of the ile")
    file_size = models.PositiveIntegerField(
        null=True, blank=True, help_text="The size of the File n bytes"
    )
    version = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="The version of the encoding schema i.e. MEI 2.0)",
    )
    encoding_date = models.DateTimeField(
        null=True, help_text="The date the File was ncoded"
    )
    encoded_with = models.ForeignKey(
        "Encoder",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The Encoder of his File",
    )
    validated_by = models.ForeignKey(
        "Validator",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The Validator of this file",
    )
    extra_metadata = JSONField(
        null=True,
        blank=True,
        help_text="Any extra metadata associated with he File",
    )
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
    def composers(self) -> QuerySet:
        """Return the composers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the composers
        """
        return self.musical_work.composers

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
    def arrangers(self) -> QuerySet:
        """Return the arrangers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the arrangers
        """
        return self.musical_work.arrangers

    @property
    def arrangers_dates(self) -> List[str]:
        """Return the arrangement dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of arrangement
        """
        return self.musical_work.arrangers_dates

    @property
    def arrangers_locations(self) -> QuerySet:
        """Return the arrangement places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was arranged
        """
        return self.musical_work.arrangers_locations

    @property
    def authors(self) -> QuerySet:
        """Return the authors of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the authors
        """
        return self.musical_work.authors

    @property
    def authors_dates(self) -> List[str]:
        """Return the authorship dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of authorship
        """
        return self.musical_work.authors_dates

    @property
    def authors_locations(self) -> QuerySet:
        """Return the authorship places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was composed
        """
        return self.musical_work.authors_locations

    @property
    def transcribers(self) -> QuerySet:
        """Return the transcribers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the transcribers
        """
        return self.musical_work.transcribers

    @property
    def transcribers_dates(self) -> List[str]:
        """Return the transcription dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of transcription
        """
        return self.musical_work.transcribers_dates

    @property
    def transcribers_locations(self) -> QuerySet:
        """Return the trasncription places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was transcribed
        """
        return self.musical_work.transcribers_locations

    @property
    def improvisers(self) -> QuerySet:
        """Return the improvisers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the improvisers
        """
        return self.musical_work.improvisers

    @property
    def improvisers_dates(self) -> List[str]:
        """Return the improvisation dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of improvisation
        """
        return self.musical_work.improvisers_dates

    @property
    def improvisers_locations(self) -> QuerySet:
        """Return the improvisation places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was improvised
        """
        return self.musical_work.improvisers_locations

    @property
    def performers(self) -> QuerySet:
        """Return the performers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the performers
        """
        return self.musical_work.performers

    @property
    def performers_dates(self) -> List[str]:
        """Return the perfomance dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of performance
        """
        return self.musical_work.performers_dates

    @property
    def performers_locations(self) -> QuerySet:
        """Return the perfomance places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was performed
        """
        return self.musical_work.performers_locations

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
