from urllib import request
import datetime
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from database.forms.creation_forms import (CollectionOfSourcesForm,
                                           ContributionForm, FileForm,
                                           WorkInfoForm)
from database.forms.source_creation_form import SourceForm
from database.models import (Contribution, GenreAsInStyle, GenreAsInType,
                             Instrument, MusicalWork, Part, Section)


class CreationView(FormView):

    template_name = 'creation_form.html'
    success_url = "/"
    ContributionFormSet = formset_factory(ContributionForm)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        form = WorkInfoForm()
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
        form = WorkInfoForm(self.request.POST)
        # I'm getting the variant titles before validation because when
        # the is_valid() method is called, the list of variant_titles is
        # is transformed onto a single value

        # TODO: check titles for SQL injections etc
        variant_titles = request.POST.getlist('variant_title')
        contribution_form = self.ContributionFormSet(self.request.POST)
        source_form = CollectionOfSourcesForm(self.request.POST)
        parent_source_form = CollectionOfSourcesForm(self.request.POST)
        if (form.is_valid() and contribution_form.is_valid() and
                source_form.is_valid() and parent_source_form.is_valid()):
            form.cleaned_data['variant_titles'] = variant_title
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
                                  contribution_forms=contribution_forms))
