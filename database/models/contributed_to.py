from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from database.models.custom_base_model import CustomBaseModel
from database.models.date_with_provenance import DateWithProvenance
from database.models.location_with_provenance import LocationWithProvenance
from database.models.person_with_provenance import PersonWithProvenance
from database.models.text_with_provenance import TextWithProvenance


class ContributedTo(CustomBaseModel):
    """Relates a person that contributed to a work/section/part

    A work/section/part can have many contributors with different roles
    i.e. a person composed a piece, two others arranged it, another wrote the
    lyrics
    A person can be related to a work, section or part, this is implemented
    using GenericForeignKeys
    """
    person = models.OneToOneField(PersonWithProvenance,
                                  on_delete=models.PROTECT, null=True,
                                  blank=True)
    role = models.OneToOneField(TextWithProvenance,
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True)
    date = models.OneToOneField(DateWithProvenance, on_delete=models.PROTECT,
                                null=True, blank=True)
    location = models.OneToOneField(LocationWithProvenance,
                                    on_delete=models.PROTECT, null=True,
                                    blank=True)

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
