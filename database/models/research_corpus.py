"""Define a ResearchCorpus model"""
from django.db import models

from database.models.custom_base_model import CustomBaseModel


class ResearchCorpus(CustomBaseModel):
    """A collection of files that can be used in specific empirical studies.

    Attributes
    ----------
    ResearchCorpus.title : models.CharField
        The title of this ResearchCorpus

    ResearchCorpus.features : models.ManyToManyField
        References to ExtractedFeatures used by this ResearchCorpus

    ResearchCorpus.creators : models.CharField
        The creators of this ResearchCorpus

    ResearchCorpus.curators : models.CharField
        The curators of this ResearchCorpus

    ResearchCorpus.files : models.ManyToManyField
        References to the SymbolicMusicFiles contained in this ResearchCorpus

    ResearchCorpus.studies : models.ManyToOneRel
        References to the studies that use this ResearchCorpus

    See Also
    --------
    database.models.CustomBaseModel
    database.models.ExtractedFeatures
    database.models.SymbolicMusicFile
    database.models.ExperimentalStudy
    """
    title = models.CharField(max_length=200,
                             blank=False,
                             help_text='The title of this Research Corpus')
    creators = models.CharField(max_length=200,
                                blank=True,
                                help_text='The creators of this '
                                          'Research Corpus')
    curators = models.CharField(max_length=200,
                                blank=True,
                                help_text='The curators of this '
                                          'Research Corpus')
    files = models.ManyToManyField('SymbolicMusicFile',
                                   related_name='in_corpora',
                                   help_text='The Symbolic Music Files that '
                                             'this Research Corpus contains')
    DOI_link = models.URLField(blank=True,
                               null=True,
                               help_text='An DOI linking to an '
                                         'research corpus '
                                         'saved in Zenodo ')
    class Meta(CustomBaseModel.Meta):
        db_table = 'research_corpus'
        verbose_name_plural = 'Research Corpora'

    def __str__(self):
        return "{0}".format(self.title)
