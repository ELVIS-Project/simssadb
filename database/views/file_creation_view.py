import datetime
from urllib import request

from django import forms
from django.forms import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from database.forms.creation_forms import (CollectionOfSourcesForm, FileForm)
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
        work_id = request.session['work_id']
        work_queryset = MusicalWork.objects.filter(pk=work_id)
        if work_queryset.exists():
            work = work_queryset[0]
            sections = work.sections.all()
            parts = work.parts

            # Here I am defining new classes dynamically.
            # It seems strange but I need to do this because the fields of a
            # form are class instances. We need a ModelChoiceField with a
            # different queryset based on the musical work that we are dealing
            # with. Therefore, I need to create the class here instead of
            # defining it beforehand. I've tried workarounds but this is the
            # best solution I've found.
            section_field = forms.ModelChoiceField(queryset=sections)
            DynamicSectionFileForm = type('SectionFileForm',
                                          (FileForm,),
                                          {'section': section_field})
            part_field = forms.ModelChoiceField(queryset=parts)
            DynamicPartFileForm = type('PartFileForm',
                                       (FileForm,),
                                       {'part': part_field})

            WorkFormSet = formset_factory(FileForm)
            work_formset = WorkFormSet(prefix='work')

            if sections.exists():
                SectionFormSet = formset_factory(DynamicSectionFileForm)
                section_formset = SectionFormSet(prefix='section')
            else:
                section_formset = None

            if parts.exists():
                PartFormSet = formset_factory(DynamicPartFileForm)
                part_formset = PartFormSet(prefix='part')
            else:
                part_formset = None
        else:
            raise Exception

        child_source_form = CollectionOfSourcesForm(prefix='child')
        parent_source_form = CollectionOfSourcesForm(prefix='parent')

        return self.render_to_response(
            self.get_context_data(work_formset=work_formset,
                                  section_formset=section_formset,
                                  part_formset=part_formset,
                                  child_source_form=child_source_form,
                                  parent_source_form=parent_source_form))

    # TODO: deal with repeated code in this method
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        work_id = request.session['work_id']
        work_queryset = MusicalWork.objects.filter(pk=work_id)
        if work_queryset.exists():
            work = work_queryset[0]
            sections = work.sections.all()
            parts = work.parts

            WorkFormSet = formset_factory(FileForm)
            work_formset = WorkFormSet(request.POST,
                                       request.FILES,
                                       prefix='work')
            if sections.exists():
                section_field = forms.ModelChoiceField(queryset=sections)
                DynamicSectionFileForm = type('SectionFileForm',
                                              (FileForm,),
                                              {'section': section_field})
                SectionFormSet = formset_factory(DynamicSectionFileForm)
                section_formset = SectionFormSet(request.POST,
                                                 request.FILES,
                                                 prefix='section')
            else:
                section_formset = None

            if parts.exists():
                part_field = forms.ModelChoiceField(queryset=parts)
                DynamicPartFileForm = type('PartFileForm',
                                           (FileForm,),
                                           {'part': part_field})
                PartFormSet = formset_factory(DynamicPartFileForm)
                part_formset = PartFormSet(request.POST,
                                           request.FILES,
                                           prefix='part')
            else:
                part_formset = None

        else:
            raise Exception

        child_source_form = CollectionOfSourcesForm(request.POST,
                                                    prefix='child')
        parent_source_form = CollectionOfSourcesForm(request.POST,
                                                     prefix='parent')

        # Forms must be valid but section_formset or part_formset can be None
        if (
            work_formset.is_valid() and
            (section_formset is None or section_formset.is_valid()) and
            (part_formset is None or part_formset.is_valid()) and
            (child_source_form.is_valid() and parent_source_form.is_valid())
           ):
            return self.form_valid(work_formset, section_formset, part_formset,
                                   child_source_form, parent_source_form)
        else:
            return self.form_invalid(work_formset, section_formset,
                                     part_formset, child_source_form,
                                     parent_source_form)

    def form_valid(self, workf_formset, section_formset, part_formset,
                   child_source_form, parent_source_form):
        """
        Called if all forms are valid.
        """
        return HttpResponseRedirect('/')

    def form_invalid(self, workf_formset, section_formset, part_formset,
                     child_source_form, parent_source_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(work_formset=work_formset,
                                  section_formset=section_formset,
                                  part_formset=part_formset,
                                  child_source_form=child_source_form,
                                  parent_source_form=parent_source_form))
