from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.source import Source


class MusicalInstance(CustomBaseModel):
    """An abstract entity defined by the music specified by a particular Source

    It corresponds to a particular instantiation of all or part of a Musical
    Work. It must have a Source, and it is manifested by files.
    The relationship to files is implemented using a GenericForeignKey
    """
    source = models.OneToOneField(Source, on_delete=models.CASCADE,
                                  related_name='source_of')
    limit = models.Q(app_label='database', model='musical_work') | models.Q(
            app_label='database', model='section') | models.Q(
            app_label='database', model='part')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    instance_of = GenericForeignKey('content_type', 'object_id')


    class Meta(CustomBaseModel.Meta):
        db_table = 'musical_instance'
