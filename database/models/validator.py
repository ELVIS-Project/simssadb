from django.db import models
from database.models.custom_base_model import CustomBaseModel
from database.models.person import Person
from database.models.software import Software


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
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    notes = models.TextField()


    class Meta(CustomBaseModel.Meta):
        db_table = 'validator_software'
