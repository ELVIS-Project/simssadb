from urllib import request

from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from database.forms.creation_form import ContributionForm, WorkInfoForm, \
    CollectionOfSourcesForm, FileForm
from database.forms.source_creation_form import SourceForm
from database.models import (GenreAsInStyle, GenreAsInType, Instrument,
                             MusicalWork, Part, Section)


class CreationView(FormView):

    template_name = 'creation_form.html'
    form_class = WorkInfoForm
    success_url = "/"
    ContributionFormSet = formset_factory(ContributionForm)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contribution_form = self.ContributionFormSet()
        collection_form = CollectionOfSourcesForm()
        file_form = FileForm()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contribution_form=contribution_form,
                                  collection_form=collection_form,
                                  file_form=file_form))
