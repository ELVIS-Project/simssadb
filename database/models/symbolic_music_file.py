import os

from django.db import models
from django.template.defaultfilters import filesizeformat

from database.models.file import File
from database.models.instrument import Instrument
from database.models.source import Source


class SymbolicMusicFile(File):
    """
    Manifestation of a Musical Instance as a digital music file

    Generated from a Source by a Symbolic Encoder
    """
    instruments_used = models.ManyToManyField(Instrument,
                                              help_text='The Instruments used '
                                                        'in this Symbolic '
                                                        'File',
                                              blank=True)

    manifests = models.ForeignKey(Source,
                                  related_name='manifested_by_sym_files',
                                  on_delete=models.CASCADE, null=False,
                                  help_text='The Source manifested by this '
                                            'Symbolic File')
    file = models.FileField(upload_to='symbolic_music/',
                            help_text='The actual file')

    def __str__(self):
        filename = os.path.basename(self.file.name)
        return "{0}".format(filename)

    @property
    def features(self):
        """Return all the features of this file

        Returns
        -------
       QuerySet
            A QuerySet of all the features extracted from this File
        """
        return self.extracted_features.all()

    @property
    def one_dimensional_features(self):
        """Return all the one dimensional features of this file

        Returns
        -------
       QuerySet
            A QuerySet of all the one dimensional features extracted from
            this File
        """
        return self.features.exclude(value__len__gt=1)

    @property
    def histograms(self):
        """Return all histograms (multi-dimensional features)

        Returns
        -------
        QuerySet
            A QuerySet of all the histograms (multidimensional features)
            extracted from this file
        """
        return self.features.exclude(value__len__lte=1)

    @property
    def musical_work(self):
        """Return the MusicalWork the Source of this File is related to

        Returns
        -------
        MusicalWork
            The MusicalWork the Source of this File is related to
        """
        return self.manifests.work

    @property
    def sections(self):
        """Return the Sections manifested in full by the Source of this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Sections the Source of this File is related to
        """
        return self.manifests.sections.all()

    @property
    def parts(self):
        """Return the Parts manifested in full by the Source of this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Parts the Source of this File is related to
        """
        return self.manifests.parts.all()

    @property
    def composers(self):
        """Return the composers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the composers
        """
        return self.musical_work.composers_queryset

    @property
    def sacred_or_secular(self):
        """Return the sacred_or_secular of the MusicalWork related to this file

        Returns
        -------
        bool
            The sacred_or_secular of the MusicalWork related to this file
        """
        return self.musical_work.sacred_or_secular

    @property
    def certainty(self):
        """Return the certainty of the MusicalWork related to this File

        Returns
        -------
        bool
            The certainty of attribution of the MusicalWork related to this File
        """
        return self.musical_work.certainty_of_attribution

    @property
    def genres_as_in_type(self):
        """Return the Genres (type) of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            The Genres (type) of the MusicalWork related to this File
        """
        return self.musical_work.genres_as_in_type.all()

    @property
    def genres_as_in_style(self):
        """Return the Genres (style) of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            The Genres (style) of the MusicalWork related to this File
        """
        return self.musical_work.genres_as_in_style.all()

    @property
    def dates_of_composition(self):
        """Return the dates of the MusicalWork related to this File

        Returns
        -------
        list
            A list of date tuples representing the date ranges of composition
        """
        return self.musical_work.dates_of_composition

    @property
    def places_of_composition(self):
        """Return the places of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of GeographicAreas where the Musical Work related to
            this File was composed
        """
        return self.musical_work.places_of_composition

    @property
    def instrumentation(self):
        """Return the Instruments of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Instruments of the MusicalWork related to this
            File
        """
        return self.musical_work.instrumentation

    @property
    def sections_are_complete(self):
        """Whether or not every Section of this File is represented completely.

        Checks whether all the Sections represented by this File also have all
        their parts represented by this File.

        Returns
        -------
        bool
            True if every Section related to this File is represented
            completely, False otherwise
        """
        for section in self.sections:
            num_parts_of_section = section.parts.count()
            # Parts of this file that are also Parts of the Section we are
            # examining at this point in the loop
            parts_of_file = [part for part in self.parts if part in
                             section.parts.all()]
            num_parts_of_file = len(parts_of_file)
            if num_parts_of_section != num_parts_of_file:
                return False
        return True

    @property
    def is_complete_work(self):
        """Whether or not this File represents the complete MusicalWork

        Returns
        -------
        bool
            True if File represents complete MusicalWork, False otherwise
        """

        # If Sections are not complete then the File cannot be the complete work
        if not self.sections_are_complete:
            return False

        num_sections_of_work = self.musical_work.sections.count()
        num_sections_of_file = self.sections.count()

        return num_sections_of_work == num_sections_of_file

    class Meta:
        db_table = 'symbolic_music_file'
