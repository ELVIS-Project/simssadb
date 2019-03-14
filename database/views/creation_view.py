from database.forms.creation_form import CreationForm
from django.views.generic import FormView


class CreationView(FormView):

    template_name = 'creation_form.html'
    form_class = CreationForm
    success_url = '/'

    def form_valid(self, form):
        print(form.data)
        return super().form_valid(form)
