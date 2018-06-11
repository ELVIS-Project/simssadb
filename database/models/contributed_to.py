from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person
from django.contrib.postgres.fields import DateRangeField
from database.models.geographic_area import GeographicArea


class ContributedTo(CustomBaseModel):
    """Relates a person that contributed to a work/section/part

    A work/section/part can have many contributors with different roles
    i.e. a person composed a piece, two others arranged it, another wrote the
    lyrics
    A person can be related to a work, section or part, this is implemented
    using GenericForeignKeys
    """
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    certain = models.BooleanField(default=True, null=False, blank=False)
    role = models.CharField(default="Composer")
    date_of_contrib = DateRangeField()
    location = models.ForeignKey(GeographicArea, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    # TODO: Remove this generic foreign key
    # Generic foreign key to allow polymorphic relation to work/section/part
    limit = models.Q(app_label='database', model='musicalwork') | models.Q(
            app_label='database', model='section') | models.Q(
            app_label='database', model='part')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    contributed_to = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return "{0}, {1} of {2}".format(self.person, self.role,
                                        self.contributed_to)


    class Meta(CustomBaseModel.Meta):
        db_table = 'contributed_to'
        verbose_name_plural = 'Contributed To Relationships'
