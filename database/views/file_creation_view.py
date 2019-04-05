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

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        work_id = request.GET.get('id')
        work_queryset = MusicalWork.objects.filter(pk=work_id)
        if work_queryset.exists():
            work = work_queryset[0]
        else:
            raise Exception
        sections = work.sections.all()
        parts = work.parts

        WorkFormSet = formset_factory(FileForm)
        work_formset = WorkFormSet(prefix='work')

        empty_form = work_formset.empty_form
        empty_form.fields["attach_to"] = forms.ModelChoiceField(
                                                        queryset=work_queryset,
                                                        required=True)
        for form in work_formset:
            form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=work_queryset,
                                                    required=True)

        if sections.exists():
            SectionFormSet = formset_factory(FileForm)
            section_formset = SectionFormSet(prefix='section')

            for form in section_formset:
                form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=sections,
                                                    required=True)
        else:
            section_formset = None

        if parts.exists():
            PartFormSet = formset_factory(FileForm)
            part_formset = PartFormSet(prefix='part')

            for form in part_formset:
                form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=parts,
                                                    required=True)
        else:
            part_formset = None
        return self.render_to_response(
                self.get_context_data(work_formset=work_formset,
                                      section_formset=section_formset,
                                      part_formset=part_formset,
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
