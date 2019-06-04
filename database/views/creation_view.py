import datetime
from urllib import request

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
                             Instrument, MusicalWork, Part, Person, Section)


class CreationView(FormView):
    template_name = 'creation_form.html'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and the formsets.
        """
        form = WorkInfoForm()
        contribution_forms = formset_factory(ContributionForm)
        return self.render_to_response(
                self.get_context_data(form=form,
                                      contribution_form=contribution_forms))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        form = WorkInfoForm(request.POST)
        contribution_formset = formset_factory(ContributionForm)
        # I'm getting the variant titles and sections before validation
        # because when the is_valid() method is called, the lists of
        # variant_titles and sections are transformed onto single values

        # TODO: check titles and sections for SQL injections etc
        variant_titles = request.POST.getlist('variant_title')
        sections = request.POST.getlist('section_title')
        contribution_forms = contribution_formset(request.POST)
        if (form.is_valid() and contribution_forms.is_valid()):
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
                           _sacred_or_secular=sacred_or_secular)
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
            # Create parts for each section
            for instrument in instruments:
                part = Part(written_for=instrument, section=section)
                part.save()
        # Create contributions
        for form in contribution_forms:
            person_given_name = form.cleaned_data['person_given_name']
            person_surname = form.cleaned_data['person_surname']
            range_date_birth = form.cleaned_data['person_range_date_birth']
            range_date_death = form.cleaned_data['person_range_date_death']
            role = form.cleaned_data['role']
            certainty = form.cleaned_data['certainty_of_attribution']
            location = form.cleaned_data['location']
            date = form.cleaned_data['date']
            if date:
                year_from = form.cleaned_data['date'].lower
                if year_from:
                    date_from = datetime.date(year_from, 1, 1)
                else:
                    date_from = None
                year_to = form.cleaned_data['date'].upper
                if year_to:
                    date_to = datetime.date(year_to, 2, 2)
                else:
                    date_to = None
            else:
                date_from, date_to = None, None

            person, created = Person.objects.get_or_create(
                                                given_name=person_given_name,
                                                surname=person_surname)
            if range_date_birth:
                birth_year_from = form.cleaned_data[
                                    'person_range_date_birth'].lower
                if birth_year_from:
                    birth_date_from = datetime.date(birth_year_from, 1, 1)
                else:
                    birth_date_from = None
                birth_year_to = form.cleaned_data[
                                    'person_range_date_birth'].upper
                if birth_year_to:
                    birth_date_to = datetime.date(birth_year_to, 2, 2)
                else:
                    birth_date_to = None
            else:
                birth_date_to, birth_date_from = None, None

            if range_date_death:
                death_year_from = form.cleaned_data[
                                    'person_range_date_death'].lower
                if death_year_from:
                    death_date_from = datetime.date(death_year_from, 1, 1)
                else:
                    death_date_from = None
                death_year_to = form.cleaned_data[
                                    'person_range_date_death'].upper
                if death_year_to:
                    death_date_to = datetime.date(death_year_to, 2, 2)
                else:
                    death_date_to = None
            else:
                death_date_from, death_date_to = None, None

            person.range_date_birth = (birth_date_from, birth_date_to)
            person.range_date_death = (death_date_from, death_date_to)
            person.save()

            contribution = Contribution(person=person,
                                        role=role,
                                        certainty_of_attribution=certainty,
                                        _date=(date_from, date_to),
                                        location=location,
                                        contributed_to_work=work)
            contribution.save()
            request.session['work_id'] = work.id
        return HttpResponseRedirect('/file_create/')

    def form_invalid(self, form, contribution_forms):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contribution_forms=contribution_forms))
