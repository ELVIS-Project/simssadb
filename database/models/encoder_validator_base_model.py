from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.auth.models import User
from database.models.software import Software
from django.core.exceptions import ValidationError


class EncoderValidatorBaseModel(CustomBaseModel):
    """A base model for Encoder and Validator
    """
    work_flow_text = models.TextField()
    work_flow_file = models.FileField(upload_to='workflows', null=True)
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             null=True, blank=True)
    software = models.ForeignKey(Software, on_delete=models.PROTECT,
                                 null=True, blank=True)


    def clean(self):
        if self.user_id is not None and self.software_id is not None:
            raise ValidationError('Both User and Software are set. One must '
                                  'be null')
        if self.user_id is None and self.software_id is None:
            raise ValidationError('Neither User and Software are set')
        super(CustomBaseModel, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CustomBaseModel, self).save()


    class Meta(CustomBaseModel.Meta):
        abstract = True
