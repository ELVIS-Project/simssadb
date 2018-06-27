from django.db import models
from database.models.custom_base_model import CustomBaseModel
from django.contrib.auth.models import User
from database.models.software import Software
from django.core.exceptions import ValidationError


class EncoderValidatorBaseModel(CustomBaseModel):
    """A base model for Encoder and Validator"""
    work_flow_text = models.TextField(help_text='A description of the '
                                                'workflow that was used to '
                                                'encode or validate a File'
                                                'in the database')
    work_flow_file = models.FileField(upload_to='workflows/', null=True,
                                      blank=True,
                                      help_text='A file that describes or '
                                                'defines the workflow that '
                                                'was used to encode or '
                                                'validate a File in the '
                                                'database')
    notes = models.TextField(null=True, blank=True,
                             help_text='Any extra notes or remarks the User '
                                       'wishes to provide')
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             null=True, blank=True,
                             help_text='The User that encoded or validated '
                                       'a File')
    software = models.ForeignKey(Software, on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 help_text='The Software the encoded or '
                                           'validated a File')


    def clean(self):
        """
        Enforces the integrity of the relationship to Person or User

        Ensures that at least one of the Person or User is not null.
        Ensures that only one of Person or User is not null.
        """
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
