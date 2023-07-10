import datetime
from urllib import request
from django.contrib.auth.decorators import login_required, permission_required
from construct import ValidationError
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.db.models import Q

from database.forms.creation_forms import (ContributionForm, FileForm,
                                           WorkInfoForm)
from database.forms.source_creation_form import SourceForm
from database.models import (ContributionMusicalWork, GenreAsInStyle, GenreAsInType,
                             Instrument, MusicalWork, Part, Person, Section)


class CreationView(FormView):
    template_name = 'creation_form.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        if not request.user.has_perm('simssadb.creation_access'):
            return redirect('/')
        
        form = WorkInfoForm()
        contribution_forms = formset_factory(ContributionForm)
        return self.render_to_response(
                self.get_context_data(error_message=None,
                                      form=form,
                                      contribution_form=contribution_forms))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        
        # I'm getting the variant titles and sections before validation
        # because when the is_valid() method is called, the lists of
        # variant_titles and sections are transformed onto single values
        form = WorkInfoForm(request.POST)
        contribution_formset = formset_factory(ContributionForm)
    
        for key, value in request.POST.items():
            print(f'{key}: {value}')
        # TODO: check titles and sections for SQL injections etc
        variant_titles = request.POST.getlist('variant_title')
        sections = request.POST.getlist('sections')
        section_titles = request.POST.getlist('select_section')
        
        if request.POST.get('title_from_db'):
            title_from_db = [MusicalWork.objects.all()[int(request.POST.get('title_from_db'))]]
        key = 0
        person_from_db = []
        while request.POST.get(f'form-{key}-person_from_db'):
            person_from_db.append(Person.objects.all().order_by("surname")[int(request.POST.get(f'form-{key}-person_from_db'))])
            key+=1
        if len(person_from_db) == 0: 
            person_from_db = None
    
        contribution_forms = contribution_formset(request.POST)
        if form.is_valid() and all(contribution_form.is_valid() for contribution_form in contribution_forms):
            # Check that form is logically valid
            if (not form.cleaned_data['title_from_db'] and not form.cleaned_data['title']):
                return self.form_invalid(form, contribution_formset(request.POST))
            for contribution_form in contribution_formset.forms:
                if (not contribution_form.cleaned_data['person_range_date_death']) or \
                (not contribution_form.cleaned_data['person_range_date_birth']) or \
                (not contribution_form.cleaned_data['person_given_name'] and not form.cleaned_data['person_from_db']):
                    return self.form_invalid(form, contribution_formset(request.POST))

            form.cleaned_data['variant_titles'] = variant_titles
            form.cleaned_data['sections'] = sections
            form.cleaned_data['section_titles'] = section_titles
            form.cleaned_data['title_from_db'] = [title_from_db]
            form.cleaned_data['person_from_db'] = [person_from_db]
            return self.form_valid(form, contribution_forms, request)
        else:
            return self.form_invalid(form, contribution_forms)
    

    def form_valid(self, form, contribution_forms, request):
        """
        Called if all forms are valid.
        """
        # Get all the data from the form
        print(form.cleaned_data)            
        variant_titles = form.cleaned_data['variant_titles']
        styles = form.cleaned_data['genre_as_in_style']
        types = form.cleaned_data['genre_as_in_type']
        instruments = form.cleaned_data['instruments']
        sacred_or_secular = form.cleaned_data['sacred_or_secular']
        if not sacred_or_secular:
            sacred_or_secular = None
        try:
            sections = form.cleaned_data['sections_from_db']
            section_titles = form.cleaned_data['select_section_from_db']
            title = form.cleaned_data['title_from_db']
            work = MusicalWork.objects.get(variant_titles__0__icontains=title)
            work.variant_titles = variant_titles + work.variant_titles
            work.save()
        except KeyError:
            title = form.cleaned_data['title']
            sections = form.cleaned_data['sections']
            section_titles = form.cleaned_data['select_section']
            titles = [title] + variant_titles
            work = MusicalWork(variant_titles=titles,
                            sacred_or_secular=sacred_or_secular)
            work.save()
            work.genres_as_in_style.set(styles)
            work.genres_as_in_type.set(types)
            work.save()            

        # Create sections
        for i in range(len(sections)):
            count = section_titles[i]
            entry = sections[i]
            section = Section(title=entry, musical_work=work)
            section.save()
            section.ordering = int(count)
            section.save()
            # Create parts for each section
            for instrument in instruments:
                part = Part(written_for=instrument, section=section)
                part.save()
        # Create contributions
        for form in contribution_forms:
            # Fetch or create the person
            if form.cleaned_data['person_from_db']:
                person = Person.objects.get(given_name=form.cleaned_data['person_from_db'])
            else:
                person_given_name = form.cleaned_data['person_given_name']
                person_surname = form.cleaned_data['person_surname']
                person, created = Person.objects.get_or_create(
                                    given_name=person_given_name,
                                    surname=person_surname)       
                range_date_birth = form.cleaned_data.get('person_range_date_birth')
                birth_date_from, birth_date_to = range_date_birth.lower, range_date_birth.upper
                range_date_death = form.cleaned_data.get('person_range_date_death')
                death_date_from, death_date_to = range_date_death.lower, range_date_death.upper
                # Old way of doing it, with datetime:
                # if date:
                #     date_from = datetime.date(form.cleaned_data['date'].lower, 1, 1) if form.cleaned_data['date'].lower else None
                #     date_to = datetime.date(form.cleaned_data['date'].upper, 1, 2) if form.cleaned_data['date'].upper else None
                # else:
                #     date_from = None
                #     date_to = None

                person.range_date_birth = (birth_date_from, birth_date_to)
                person.range_date_death = (death_date_from, death_date_to)
                person.save()
            
            role = form.cleaned_data.get('role')
            certainty = form.cleaned_data.get('certainty_of_attribution')
            location = form.cleaned_data.get('location')
            date = form.cleaned_data.get('date')
            date_from, date_to = date.lower, date.upper
            
            contribution = ContributionMusicalWork(person=person,
                                        role=role,
                                        certainty_of_attribution=certainty,
                                        date_range_year_only=(date_from, date_to),
                                        location=location,
                                        contributed_to_work=work)
            contribution.save()
            request.session['work_id'] = work.id
        return HttpResponseRedirect('/file-create/')

    def form_invalid(self, form, contribution_forms):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        print(form.errors)
        for contributionform in contribution_forms:
            print(contributionform.errors)
        error_message = "Please correct the form before resubmitting. All fields marked with * are required. For date ranges, if the date is known, you may enter it in a single box."
        return self.render_to_response(
            self.get_context_data(error_message=error_message,
                                  form=form,
                                  contribution_form=contribution_forms))
    
