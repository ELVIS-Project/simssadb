from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.extracted_feature import ExtractedFeature
from django.contrib.auth.models import User


class ResearchCorpus(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    features = models.ManyToManyField(ExtractedFeature)
    creators = models.ManyToManyField(User, related_name='created_corpora')
    curators = models.ManyToManyField(User, related_name='curated_corpora')


    class Meta(CustomBaseModel.Meta):
        db_table = 'research_corpus'
