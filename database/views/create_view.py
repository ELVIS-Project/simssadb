from django.shortcuts import render
from django.views.generic import FormView
from database.forms.forms import MusicalWorkForm
from database.forms.forms import GenreStyleForm
from database.forms.forms import GenreTypeForm
from database.forms.forms import PersonForm
from database.forms.forms import ContributionForm
from database.forms.forms import PartForm


class CreateMusicalWorkView_Custom(FormView):
    template_name = 'musical_work_form.html'

    def get(self, request, *args, **kwargs):

        context = {
            'musical_work_form': MusicalWorkForm,
            'style_form': GenreStyleForm,
            'type_form': GenreTypeForm,
            'person_form': PersonForm,
            'contribution_form': ContributionForm,
            'part_form': PartForm
        }
        return render(request, self.template_name, context)
