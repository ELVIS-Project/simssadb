from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.research_corpus import ResearchCorpus


class FileInResearchCorpus(CustomBaseModel):
    research_corpus = models.ForeignKey(ResearchCorpus,
                                        on_delete=models.CASCADE)

    limit = models.Q(app_label='database', model='audio_file') | \
            models.Q(app_label='database', model='symbolic_music_file') | \
            models.Q(app_label='database', model='image_file')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    file = GenericForeignKey('content_type', 'object_id')


    class Meta(CustomBaseModel.Meta):
        db_table = 'file_in_research_corpus'
