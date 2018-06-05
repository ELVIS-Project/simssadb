from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person


class Validator(CustomBaseModel):
    class Meta:
        abstract = True


class ValidatorPerson(Validator):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    work_flow = models.TextField()
    notes = models.TextField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'validator_person'


class ValidatorSoftware(Validator):
    configuration_file = models.FileField()
    notes = models.TextField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'validator_software'
