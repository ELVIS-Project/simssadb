from django.views.generic import FormView

from database.forms.musical_work_creation_forms import *


class MusicalWorkCreationView(FormView):
    template_name = 'creation_form.html'
    form_class = MusicalWorkCreationForm
    success_url = '/'

    def form_valid(self, form):
        print(form.data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
