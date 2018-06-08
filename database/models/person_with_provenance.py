from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person


class PersonWithProvenance(CustomBaseModel):

    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    provenance = models.CharField(max_length=200, null=False, blank=True,
                                  help_text="This is where you enter where "
                                            "you got the information from")

    def __str__(self):
        return "{0}:{1}".format(self.person, self.provenance)

    class Meta(CustomBaseModel.Meta):
        db_table = 'person_with_provenance'
