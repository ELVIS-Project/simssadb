from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from database.models import ContributedTo
from database.models import GenreAsInStyle
from database.models import GeographicArea
from database.models import Instrument
from database.models import Part
from database.models import Person
from database.models import Section
from database.models import Source
from database.models.genre_as_in_type import GenreAsInType
from database.widgets.contribution_widget import MultiFieldWidget


class ContributionField(forms.MultiValueField):
    def __init__(self, **kwargs):
        choices = ContributedTo.ROLES
        fields = (
            forms.ChoiceField(choices=choices, label='Role'),
            forms.ModelChoiceField(queryset=Person.objects.all(),
                                   label='Person'),
            forms.IntegerField(min_value=1, label='Date Start', ),
            forms.IntegerField(min_value=1, label='Date End', ),
            forms.ModelChoiceField(queryset=GeographicArea.objects.all(),
                                   label='Location')
            )

        widgets = [field.widget for field in fields]

        self.widget = MultiFieldWidget(field_widgets=widgets)
        super(ContributionField, self).__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        return data_list


class FileWithInfoField(forms.MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            # forms.FileField(),
            forms.BooleanField(),
            forms.ModelChoiceField(queryset=Source.objects.all().
                                   prefetch_related('part_of_collection')),
            forms.ModelChoiceField(queryset=Section.objects.all()),
            forms.ModelChoiceField(queryset=Part.objects.all()
                                   .prefetch_related('written_for'))
            )
        widgets = [field.widget for field in fields]

        self.widget = MultiFieldWidget(field_widgets=widgets)
        super(FileWithInfoField, self).__init__(fields=fields, **kwargs)

    def compress(self, data_list):
        return data_list


class MusicalWorkCreationForm(forms.Form):
    title = SimpleArrayField(base_field=forms.CharField(max_length=100),
                             delimiter='/')
    contribution = ContributionField()
    file = FileWithInfoField()
    genres_as_in_style = forms.ModelMultipleChoiceField(
            queryset=GenreAsInStyle.objects.all())
    genres_as_in_type = forms.ModelMultipleChoiceField(
            queryset=GenreAsInType.objects.all())
    test_num = forms.IntegerField(min_value=1, initial=1400)
    instrument_0 = forms.ModelChoiceField(queryset=Instrument.objects.all())
    section_title = forms.CharField(max_length=100)
    ordering = forms.IntegerField(min_value=1)
    
    def clean(self):
        instruments = set()
        i = 1
        field_name = 'instrument_%s' % (i,)
        while self.cleaned_data.get(field_name):
            instrument = self.cleaned_data[field_name]
            print(instrument)
            instruments.add(instrument)
            i += 1
            field_name = 'instrument_%s' % (i,)
        self.cleaned_data['instruments'] = instruments
    
    def get_instruments_fields(self):
        print('Hello!')
        print(self.fields)
        for field_name in self.fields:
            if field_name.startswith('instrument_'):
                yield self[field_name]
