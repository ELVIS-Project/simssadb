from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import DateRangeField
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person
from database.models.geographic_area import GeographicArea


class ContributedTo(CustomBaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    limit = models.Q(app_label='database', model='musical_work') | \
            models.Q(app_label='database', model='section') | \
            models.Q(app_label='database', model='part')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    contributed_to = GenericForeignKey('content_type', 'object_id')

    role = models.CharField(max_length=50, null=False, blank=False,
                            default='Composer')
    date = DateRangeField()
    location = models.ForeignKey(GeographicArea, on_delete=models.SET_NULL,
                                 null=True)


    class Meta(CustomBaseModel.Meta):
        db_table = 'contributed_to'
