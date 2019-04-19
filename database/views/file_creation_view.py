import datetime
from urllib import request

from django import forms
from django.forms import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from database.forms.creation_forms import (CollectionOfSourcesForm, FileForm,
                                           SectionFileForm, PartFileForm)
from database.forms.source_creation_form import SourceForm
from database.models import (Contribution, GenreAsInStyle, GenreAsInType,
                             Instrument, MusicalWork, Part, Section)


class FileCreationView(FormView):
    template_name = 'file_creation_form.html'
    form_class = FileForm
    WorkFormSet = formset_factory(FileForm)
    SectionFormSet = formset_factory(FileForm)
    PartFormSet = formset_factory(FileForm)
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
            sections = work.sections.all()
            parts = work.parts
            work_formset = WorkFormSet(prefix='work')
            for form in work_formset:
                form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=work_queryset,
                                                    required=True)
        else:
            raise Exception

        if sections.exists():
            section_formset = SectionFormSet(prefix='section')

            for form in section_formset:
                form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=sections,
                                                    required=True)
        else:
            section_formset = None

        if parts.exists():
            part_formset = PartFormSet(prefix='part')

            for form in part_formset:
                form.fields["attach_to"] = forms.ModelChoiceField(
                                                    queryset=parts,
                                                    required=True)
        else:
            part_formset = None

        child_source_form = CollectionOfSourcesForm(prefix='child')
        parent_source_form = CollectionOfSourcesForm(prefix='parent')

        return self.render_to_response(
                self.get_context_data(work_formset=work_formset,
                                      section_formset=section_formset,
                                      part_formset=part_formset,
                                      child_source_form=child_source_form,
                                      parent_source_form=parent_source_form))

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
