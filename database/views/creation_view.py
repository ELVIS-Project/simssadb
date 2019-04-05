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
        form = WorkInfoForm(self.request.POST)
        contribution_formset = formset_factory(ContributionForm)
        # I'm getting the variant titles and sections before validation
        # because when the is_valid() method is called, the lists of
        # variant_titles and sections are transformed onto single values

        # TODO: check titles and sections for SQL injections etc
        variant_titles = request.POST.getlist('variant_title')
        sections = request.POST.getlist('section_title')
        contribution_forms = contribution_formset(self.request.POST)
        if (form.is_valid() and contribution_forms.is_valid()):
            form.cleaned_data['variant_titles'] = variant_titles
            form.cleaned_data['sections'] = sections
            return self.form_valid(form, contribution_forms)
        else:
            return self.form_invalid(form, contribution_forms)

    def form_valid(self, form, contribution_forms):
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
        for entry in sections:
            section = Section(title=entry, musical_work=work)
            section.save()
            # Create parts for each section
            for instrument in instruments:
                part = Part(written_for=instrument, section=section)
                part.save()
        # Create contributions
        for form in contribution_forms:
            person = form.cleaned_data['person']
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

            contribution = Contribution(person=person,
                                        role=role,
                                        certainty_of_attribution=certainty,
                                        _date=(date_from, date_to),
                                        location=location,
                                        contributed_to_work=work)
            contribution.save()
        return HttpResponseRedirect('/musicalworks/' + str(work.id))

    def form_invalid(self, form, contribution_forms):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  contribution_forms=contribution_forms))
