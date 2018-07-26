from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.extracted_feature import ExtractedFeature
from database.models.symbolic_music_file import SymbolicMusicFile
from django.contrib.auth.models import User


class ResearchCorpus(CustomBaseModel):
    """A collection of files that can be used in specific empirical studies"""
    title = models.CharField(max_length=200, blank=False,
                             help_text='The title of this Research Corpus')
    features = models.ManyToManyField(ExtractedFeature,
                                      help_text='The features that this '
                                                'Research Corpus contains')
    creators = models.CharField(max_length=200,
                                help_text='The creators of this '
                                          'Research Corpus')
    curators = models.CharField(max_length=200,
                                help_text='The curators of this '
                                          'Research Corpus')
    files = models.ManyToManyField(SymbolicMusicFile,
                                   help_text='The Symbolic Music Files that '
                                             'this Research Corpus contains')

    def __str__(self):
        return "{0}".format(self.title)

    def prepare_summary(self):
        summary = {'display': self.__str__(),
                   'url': self.get_absolute_url(),
                   'files_count': self.files.count()
                   }
        return summary

    class Meta(CustomBaseModel.Meta):
        db_table = 'research_corpus'
        verbose_name_plural = 'Research Corpora'
