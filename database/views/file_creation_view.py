import datetime
from urllib import request

from django import forms
from django.forms import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.views.generic import FormView
from database.forms.forms import SourcesForm
from database.forms.creation_forms import FileForm, SourceForm
from database.models import (ContributionMusicalWork, GenreAsInStyle, GenreAsInType,
                             Instrument, MusicalWork, Part, Section, Archive)
from database.models.source_instantiation import SourceInstantiation
from database.models import (Source, File,
                             Software)
from django.db.models import Q


class FileCreationView(FormView):
    template_name = 'file_creation_form.html'
    form_class = FileForm
    success_url = "musical-work-create/"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        work_id = request.session['work_id']
        work_queryset = MusicalWork.objects.filter(pk=work_id)
        if not work_queryset.exists(): 
            raise Exception
        
        work = work_queryset[0]
        sections = work.sections.all()
        parts = Part.objects.filter(Q(section__in=sections) | Q(musical_work=work))

        # Here I am defining new classes dynamically.
        # It seems strange but I need to do this because the fields of a
        # form are class instances. We need a ModelChoiceField with a
        # different queryset based on the musical work that we are dealing
        # with. Therefore, I need to create the class here instead of
        # defining it beforehand. I've tried workarounds but this is the
        # best solution I've found.
        section_field = forms.ModelChoiceField(queryset=sections, required=False)
        DynamicSectionFileForm = type('SectionFileForm',
                                        (FileForm,),
                                        {'section': section_field})
        part_field = forms.ModelChoiceField(queryset=parts, required=False)
        DynamicPartFileForm = type('PartFileForm',
                                    (FileForm,),
                                    {'part': part_field})

        WorkFormSet = formset_factory(FileForm)
        work_formset = WorkFormSet(prefix='work')
        if sections.exists():
            SectionFormSet = formset_factory(DynamicSectionFileForm)
            section_formset = SectionFormSet(prefix='section')
            # Styling
            for form in section_formset:
                for field_name, field in form.fields.items():
                    widget = field.widget
                    widget.attrs['class'] = 'form-control'
        else:
            section_formset = None

        if parts.exists():
            PartFormSet = formset_factory(DynamicPartFileForm)
            part_formset = PartFormSet(prefix='part')
            for form in part_formset:
                for field_name, field in form.fields.items():
                    widget = field.widget
                    widget.attrs['class'] = 'form-control'
        else:
            part_formset = None

        child_source_form = SourceForm(prefix='child')
        parent_source_form = SourceForm(prefix='parent')
                    
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
            parts = Part.objects.filter(Q(section__in=sections) | Q(musical_work=work))

            WorkFormSet = formset_factory(FileForm)
            work_formset = WorkFormSet(request.POST,
                                       request.FILES,
                                       prefix='work')
            if sections.exists():
                section_field = forms.ModelChoiceField(queryset=sections, required=False)
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
                part_field = forms.ModelChoiceField(queryset=parts, required=False)
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
        
        child_source_form = SourceForm(request.POST, prefix='child')
        parent_source_form = SourceForm(request.POST, prefix='parent')

        # Forms must be valid but section_formset or part_formset can be None
        # Or, if user is only inputting metadata, work_formset can be None
        if ((work_formset is None or work_formset.is_valid()) and
            (section_formset is None or section_formset.is_valid()) and
            (part_formset is None or part_formset.is_valid()) and
            (child_source_form.is_valid()) and 
            (parent_source_form.is_valid() or parent_source_form is None)) or \
            (request.POST.get('work-0-file') == '' and request.POST.get('section-0-file') == '' and request.POST.get('part-0-file') == ''):
            if request.POST.get('work-0-file') == '' and request.POST.get('section-0-file') == '' and request.POST.get('part-0-file') == '':
                return self.form_empty(work)
            
            return self.form_valid(work_formset, section_formset, part_formset,
                                   child_source_form, parent_source_form, work,
                                   sections, parts)
        else:
            if not (section_formset is None or section_formset.is_valid()):
                return self.form_invalid(work_formset, section_formset,
                                     part_formset, child_source_form,
                                     parent_source_form, error_message="The required information for Section needs to be filled out.")
            return self.form_invalid(work_formset, section_formset,
                                     part_formset, child_source_form,
                                     parent_source_form)

    def form_valid(self, work_formset, section_formset, part_formset,
                   child_source_form, parent_source_form, work, sections,
                   parts):
        """
        Called if all forms are valid.
        """
        parent_source_title = parent_source_form.cleaned_data.get('title') 
        if parent_source_title:
            parent_source_url = parent_source_form.cleaned_data.get('source_url')
            parent_archive = parent_source_form.cleaned_data.get('archive')
            try:
                parent_source = Source(title=parent_source_title, parent_source=None, url=parent_source_url)
                parent_source.save()
                if parent_archive:
                    parent_archive = Archive(name=parent_archive)
                    parent_source.in_archive = parent_archive
            except ValidationError as e:
                print(f'parent source not given: {e}')
                parent_source = None
        else:
            parent_source = None
        
        child_source_title = child_source_form.cleaned_data.get('title')
        child_source_url = child_source_form.cleaned_data.get('source_url')
        child_archive = child_source_form.cleaned_data.get('archive')

        try:
            child_source = Source(title=child_source_title, parent_source=parent_source,
                                               url=child_source_url)
            child_source.save()
            if parent_source:
                parent_source.child_source = child_source
        except ValidationError as e:
            print(f'child source not given: {e}')
            child_source = None

        if child_archive:
            child_archive = Archive(name=child_archive)
            child_source.in_archive = child_archive

        for form in work_formset:
            file = form.cleaned_data.get('file')
            if not file:
                continue
            file_format = file.name.split('.')[-1]
            file_type = form.cleaned_data.get('file_type')
            software = form.cleaned_data.get('software')
            if software:
                        software = Software.objects.get_or_create(software=software)[0]
            else:
                software = None
            encoding_date = datetime.datetime.now()
            try:
                instantiation = SourceInstantiation(source=child_source,
                                                    work=work)
                instantiation.save()
            except ValidationError as e:
                print(f'source instance information not given: {e}')
                return self.form_invalid(work_formset, section_formset,
                                     part_formset, child_source_form,
                                     parent_source_form, error_message="The required information for Source needs to be filled out.")
            try:
                file = File(file=file, instantiates=instantiation, 
                        file_type=file_type,
                        file_format=file_format,
                        encoding_date=encoding_date,
                        encoding_workflow=software)
                file.save()
                print('File saved successfully!')
            except ValidationError as e:
                print(f'file information not given: {e}')
                return self.form_invalid(work_formset, section_formset,
                                     part_formset, child_source_form,
                                     parent_source_form, error_message="The required information for File was not inputted correctly. Please ensure the file type is either Symbolic file, Audio, Text, or Image.")
        if section_formset:
            for form in section_formset:
                if 'section' in form.cleaned_data:
                    section = form.cleaned_data.get('section')
                    file = form.cleaned_data.get('file')
                    if not file:
                        continue
                    file_format = file.name.split('.')[-1]
                    file_type = form.cleaned_data.get('file_type')
                    software = form.cleaned_data.get('software')
                    if software:
                        software = Software.objects.get_or_create(software=software)[0]
                    else:
                        software = None
                    encoding_date = datetime.datetime.now()
                    try:
                        instantiation = SourceInstantiation(source=child_source)
                        instantiation.save()
                        section_object = Section.objects.get(pk=section.id)
                        instantiation.sections.set([section_object])
                        instantiation.save()
                    except ValidationError as e:
                        print(f'source instance information not given: {e}')
                        return self.form_invalid(work_formset, section_formset,
                                            part_formset, child_source_form,
                                            parent_source_form, error_message="The required information for Source needs to be filled out.")
                    try:
                        file = File(file=file, instantiates=instantiation,
                                            file_type=file_type, file_format=file_format,
                                            encoding_date=encoding_date,
                                            encoding_workflow=software)
                        file.save()
                        print('File saved successfully!')
                    except ValidationError as e:
                        print(f'file information not given: {e}')
                        return self.form_invalid(work_formset, section_formset,
                                            part_formset, child_source_form,
                                            parent_source_form, error_message="The required information for File was not inputted correctly. Please ensure the file type is either Symbolic file, Audio, Text, or Image.")
        
        if part_formset:
            for form in part_formset:
                if 'part' in form.cleaned_data:
                    part = form.cleaned_data.get('part')
                    file = form.cleaned_data.get('file')
                    if not file:
                        continue
                    file_format = file.name.split('.')[-1]
                    file_type = form.cleaned_data.get('file_type')
                    software = form.cleaned_data.get('software')
                    if software:
                        software = Software.objects.get_or_create(software=software)[0]
                    else:
                        software = None
                    encoding_date = datetime.datetime.now()
                    try:
                        instantiation = SourceInstantiation(source=child_source)
                        instantiation.save()
                        part_object = Part.objects.get(pk=part.id)
                        instantiation.parts.set([part_object])
                        instantiation.save()
                    except ValidationError as e:
                        print(f'part instance information not given: {e}')
                        return self.form_invalid(work_formset, section_formset,
                                            part_formset, child_source_form,
                                            parent_source_form, error_message="The required information for Source needs to be filled out.")
                    try:
                        file = File(file=file, instantiates=instantiation,
                                            file_type=file_type, file_format=file_format,
                                            encoding_date=encoding_date,
                                            encoding_workflow=software)
                        file.save()
                        print('File saved successfully!')
                    except ValidationError as e:
                        print(f'file information not given: {e}')
                        return self.form_invalid(work_formset, section_formset,
                                            part_formset, child_source_form,
                                            parent_source_form, error_message="The required information for File was not inputted correctly. Please ensure the file type is either Symbolic file, Audio, Text, or Image.")
        

        work_id = work.id
        return HttpResponseRedirect('/musicalworks/' + str(work_id))

    def form_invalid(self, work_formset, section_formset, part_formset,
                     child_source_form, parent_source_form, error_message=None):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        print('File form invalid')
        return self.render_to_response(
            self.get_context_data(work_formset=work_formset,
                                  section_formset=section_formset,
                                  part_formset=part_formset,
                                  child_source_form=child_source_form,
                                  parent_source_form=parent_source_form, 
                                  error_message=error_message))

    def form_empty(self, work):
        work_id = work.id
        return HttpResponseRedirect('/musicalworks/' + str(work_id))
    