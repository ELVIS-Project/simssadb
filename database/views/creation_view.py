import datetime
from urllib import request
from django.contrib.auth.decorators import login_required, permission_required
from construct import ValidationError
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

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
        
        # Sanity check that the form has been submitted and this isn't an ajax call
        if request.POST.get('newObjectForAutocomplete') == 'True':
            return self.form_invalid(form, contribution_forms)
        
        # I'm getting the variant titles and sections before validation
        # because when the is_valid() method is called, the lists of
        # variant_titles and sections are transformed onto single values
        form = WorkInfoForm(request.POST)
        contribution_formset = formset_factory(ContributionForm)
        # TODO: check titles and sections for SQL injections etc
        variant_titles = request.POST.getlist('variant_title')
        sections = request.POST.getlist('section_title')
        contribution_forms = contribution_formset(request.POST)
        if form.is_valid() and all(contribution_form.is_valid() for contribution_form in contribution_forms):
            form.cleaned_data['variant_titles'] = variant_titles
            form.cleaned_data['sections'] = sections
            return self.form_valid(form, contribution_forms, request)
        else:
            return self.form_invalid(form, contribution_forms)

    def form_valid(self, form, contribution_forms, request):
        """
        Called if all forms are valid.
        """
        # Get all the data from the form
        title = form.cleaned_data['title']
        variant_titles = form.cleaned_data['variant_titles']
        styles = form.cleaned_data['genre_as_in_style']
        types = form.cleaned_data['genre_as_in_type']
        instruments = form.cleaned_data['instruments']
        sacred_or_secular = form.cleaned_data['sacred_or_secular']
        if not sacred_or_secular:
            sacred_or_secular = None
        sections = form.cleaned_data['sections']

        # Create a musical work
        titles = [title] + variant_titles
        work = MusicalWork(variant_titles=titles,
                           sacred_or_secular=sacred_or_secular)
        work.save()
        work.genres_as_in_style.set(styles)
        work.genres_as_in_type.set(types)
        work.save()

        # Create sections
        for count, entry in enumerate(sections, start=1):
            if entry == "":
                entry = title + " Section " + str(count)
            section = Section(title=entry, musical_work=work)
            section.save()
            section.ordering = count
            section.save()
            # Create parts for each section
            for instrument in instruments:
                part = Part(written_for=instrument, section=section)
                part.save()
        # Create contributions
        for form in contribution_forms:
            person_given_name = form.cleaned_data['person_given_name']
            person_surname = form.cleaned_data['person_surname']
            person, created = Person.objects.get_or_create(
                                    given_name=person_given_name,
                                    surname=person_surname)       
            role = form.cleaned_data.get('role')
            certainty = form.cleaned_data.get('certainty_of_attribution')
            location = form.cleaned_data.get('location')
            date = form.cleaned_data.get('date')
            date_from, date_to = date.lower, date.upper
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
        # TODO: this resets the contribution form, but it should be using the form in the post request, but it doesn't work
        error_message = "Please correct the form before resubmitting. All fields marked with * are required. For date ranges, if the date is known, you may enter it in a single box."
        # I have no idea why but printing form lets it be passed to template properly, otherwise widgets for form do not render
        print(form.errors) 
        return self.render_to_response(
            self.get_context_data(error_message=error_message,
                                  form=form,
                                  contribution_form=contribution_forms))
    
