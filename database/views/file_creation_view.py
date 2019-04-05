from urllib import request
import datetime
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from django.forms import BaseFormSet
from django import forms
from database.forms.creation_forms import FileForm, CollectionOfSourcesForm
from database.forms.source_creation_form import SourceForm
from database.models import (Contribution, GenreAsInStyle, GenreAsInType,
                             Instrument, MusicalWork, Part, Section)


class FileCreationView(FormView):
    template_name = 'file_creation_form.html'
    form_class = FileForm
    success_url = "/"
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        pass

    def form_valid(self, form, contribution_forms):
        """
        Called if all forms are valid.
        """
        pass

    def form_invalid(self, form, contribution_forms):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        pass
