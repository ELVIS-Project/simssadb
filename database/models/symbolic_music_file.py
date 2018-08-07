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
                                                        'in this Symbolic File')

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

    def _prepare_summary(self):
        summary = {
            'display':   self.__str__(),
            'file_type': self.file_type,
            'source':    self.manifests,
            'url':       self.get_absolute_url()
            }
        return summary

    def get_related(self):
        related = {
            'features': {
                'list':        self.one_dimensional_features,
                'model_name':  'Features',
                'model_count': self.one_dimensional_features.count()
                }
            }
        return related

    def detail(self):
        detail_dict = {
            'title':          self.__str__(),
            'file_type':      self.file_type,
            'version':        self.version,
            'file_size':      filesizeformat(self.file.size),
            'encoding_date':  self.encoding_date,
            'encoded_with':   self.encoded_with,
            'validated_by':   self.validated_by,
            'extra_metadata': self.extra_metadata,
            'source':         self.manifests,
            'file':           self.file,
            # TODO: update how this is handled so it's more secure
            'related':        self.get_related()
            }

        return detail_dict

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
        return self.features.exclude(value__len__lt=1)

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
        return self.manifests.sections

    @property
    def parts(self):
        """Return the Parts manifested in full by the Source of this File

        Returns
        -------
        QuerySet
            A QuerySet of all the Parts the Source of this File is related to
        """
        return self.manifests.sections

    @property
    def composers(self):
        """Return the composers of the MusicalWork related to this File

        Returns
        -------
        list
            A list of strings representing the names of the composers
        """
        return self.musical_work.composers

    @property
    def religiosity(self):
        """Return the religiosity of the MusicalWork related to this file

        Returns
        -------
        bool
            The religiosity of the MusicalWork related to this file
        """
        return self.musical_work.religiosity

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
        return self.musical_work.genres_as_in_type

    @property
    def genres_as_in_style(self):
        """Return the Genres (style) of the MusicalWork related to this File

        Returns
        -------
        QuerySet
            The Genres (style) of the MusicalWork related to this File
        """
        return self.musical_work.genres_as_in_style

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
    def is_complete_work(self):
        """Whether or not this File represents the complete MusicalWork

        Returns
        -------
        bool
            True if File represents complete MusicalWork, False otherwise
        """
        num_sections_of_work = self.musical_work.sections.count()
        num_sections_of_file = self.sections.count()

        return num_sections_of_work == num_sections_of_file

    # TODO: add comparison between sections and parts to determine if it is
    # complete

    class Meta:
        db_table = 'symbolic_music_file'
