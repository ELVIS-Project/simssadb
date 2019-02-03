from django.shortcuts import render
from django.views.generic import FormView
from database.forms.forms import MusicalWorkForm
from database.forms.forms import GenreStyleForm
from database.forms.forms import GenreTypeForm
from database.forms.forms import PersonForm
from database.forms.forms import ContributionForm
from database.forms.forms import PartForm
from database.forms.forms import CollectionOfSourcesForm
from database.forms.forms import SourcesForm
from database.forms.forms import SectionForm
from django.http import HttpResponseRedirect


class CreateMusicalWorkView_Custom(FormView):
    template_name = 'musical_work_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            'musical_work_form': MusicalWorkForm,
            'style_form': GenreStyleForm,
            'type_form': GenreTypeForm,
            'person_form': PersonForm,
            'contribution_form': ContributionForm,
            'part_form': PartForm,
            'collection_of_sources_form': CollectionOfSourcesForm,
            'sources_form': SourcesForm,
            'section_form': SectionForm
        }

        return render(request, self.template_name, context)

    # render an empty form and submit it must be handled by the same class-based view, which calls the html!
    # In this case, it is CreateMusicalWorkView_Custom
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print('data needs to be processed!')
            # create a form instance and populate it with data from the request:
            # form = MusicalWorkForm(request.POST)
            # # check whether it's valid:
            # if form.is_valid():
            #     # process the data in form.cleaned_data as required
            #     # ...
            #     # redirect to a new URL:
            #     return HttpResponseRedirect('/musicalworks/')