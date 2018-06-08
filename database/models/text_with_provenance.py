from django.db import models
from database.models.custom_base_model import CustomBaseModel


class TextWithProvenance(CustomBaseModel):

    text = models.CharField(max_length=200, null=False, blank=True)
    provenance = models.CharField(max_length=200, null=False, blank=True,
                                  help_text="This is where you enter where "
                                            "you got the information from")

    def __str__(self):
        return "{0}:{1}".format(self.text, self.provenance)

    class Meta(CustomBaseModel.Meta):
        db_table = 'text_with_provenance'
