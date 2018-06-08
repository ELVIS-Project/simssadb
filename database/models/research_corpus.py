from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.extracted_feature import ExtractedFeature
from database.models.audio_file import AudioFile
from database.models.symbolic_music_file import SymbolicMusicFile
from database.models.image_file import ImageFile
from django.contrib.auth.models import User
from gm2m import GM2MField


class ResearchCorpus(CustomBaseModel):
    """A collection of files that can be used in specific empirical studies"""
    title = models.CharField(max_length=200, blank=False)
    features = models.ManyToManyField(ExtractedFeature)
    creators = models.ManyToManyField(User, related_name='created_corpora')
    curators = models.ManyToManyField(User, related_name='curated_corpora')
    files = GM2MField(AudioFile, SymbolicMusicFile, ImageFile)

    def __str__(self):
        return "{0}".format(self.title)

    class Meta(CustomBaseModel.Meta):
        db_table = 'research_corpus'
        verbose_name_plural = 'Research Corpora'
