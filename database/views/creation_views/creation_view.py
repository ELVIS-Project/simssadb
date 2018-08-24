from django.shortcuts import render
from django.views.generic import FormView

from database.forms.musical_work_creation_forms import *

class CreationView(FormView):
    template_name = 'creation_form.html'

    def get(self, request, *args, **kwargs):
        musical_work_form = MusicalWorkCreationForm()
        section_form = SectionCreationForm()
        contribution_form = ContributionCreationForm()
        file_form = FileCreationForm()

        context = {
            'work': musical_work_form,
            'section': section_form,
            'contribution': contribution_form,
            'file': file_form
            }

        return render(request, self.template_name, context)
