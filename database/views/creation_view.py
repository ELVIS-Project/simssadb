from urllib import request
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.views import View
from database.forms.creation_form import (ContributionForm, WorkInfoForm,
                                          CollectionOfSourcesForm, FileForm)
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
        source_form = CollectionOfSourcesForm()
        parent_source_form = CollectionOfSourcesForm()
        return self.render_to_response(
                self.get_context_data(form=form,
                                      contribution_form=contribution_form,
                                      source_form=source_form,
                                      parent_source_form=parent_source_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        contribution_form = self.ContributionFormSet(self.request.POST)
        source_form = CollectionOfSourcesForm(self.request.POST)
        parent_source_form = CollectionOfSourcesForm(self.request.POST)
        if (form.is_valid() and contribution_form.is_valid() and
                source_form.is_valid() and parent_source_form.is_valid()):
            return self.form_valid(form, contribution_form, source_form,
                                   parent_source_form)
        else:
            return self.form_invalid(form, contribution_form, source_form,
                                     parent_source_form)

    def form_valid(self, form, contribution_form, source_form,
                   parent_source_form):
        """
        Called if all forms are valid.
        """
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, contribution_form, source_form,
                     parent_source_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contribution_form=contribution_form,
                                  source_form=source_form,
                                  parent_source_form=parent_source_form))
