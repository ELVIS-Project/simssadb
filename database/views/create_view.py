import pprint
from pprint import pprint
from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from psycopg2.extras import DateRange

from database.forms.forms import CollectionOfSourcesForm, ContributionForm, \
    GenreStyleForm, GenreTypeForm, MusicalWorkForm, PartForm, PersonForm, \
    SectionForm, SourcesForm
from database.models import MusicalWork, Contribution


class CreateMusicalWorkViewCustom(FormView):
    template_name = 'musical_work_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            'musical_work_form':          MusicalWorkForm,
            'style_form':                 GenreStyleForm,
            'type_form':                  GenreTypeForm,
            'person_form':                PersonForm,
            'contribution_form':          ContributionForm,
            'part_form':                  PartForm,
            'collection_of_sources_form': CollectionOfSourcesForm,
            'sources_form':               SourcesForm,
            'section_form':               SectionForm
        }

        return render(request, self.template_name, context)

    # In this case, it is CreateMusicalWorkView_Custom
    def post(self, request, *args, **kwargs):
        # the required title of the musical work is named as "title",
        # and other variant titles will be names as
        # "titlex" the required role of the person will be called as "role",
        # for more persons, it will be named as
        # "rolex" the selected id for the source will be called as
        # "collection" the selected id for the person will
        # be called as "person_selected" and for more persons, it will be
        # named as instrumentation will be called
        # "wirtten_for" the titles of the new source and the new section will
        # be called as "title_source" and
        # "title_section", respectively certainty of attribution will be
        # called "certainty_of_attribution_yesx" and
        # "certainty_of_attribution_nox" contribution date will be called as
        # "contribution_start_datex" and
        # "contribution_start_endx" for location, institution and instrument
        # where the user can create on the fly by
        # inputting the name, the corresponding field in POST request will be
        # the name, rather than the id number
        # the example below is the test case to create the most simple
        # instance of a musical work
        # form = MusicalWorkForm(variant_titles)
        # create a form instance and populate it with data from the request:
        # form = MusicalWorkForm(request.POST)
        # # check whether it's valid:
        # if form.is_valid():
        #     # process the data in form.cleaned_data as required
        #     # ...
        #     # redirect to a new URL:
        pprint(request.POST)
        post_dict = request.POST

        variant_titles = []
        contribution_end_dates = []
        contribution_start_dates = []
        given_names = []
        persons_selected = []
        person_authority_control_urls = []
        range_date_births = []
        range_date_deaths = []
        roles = []
        surnames = []
        section_titles = []
        certainties_of_attribution_yes = []
        certainties_of_attribution_no = []

        for key, value in post_dict.items():
            if key.startswith('title') and not (
                    key.startswith('title_section') or
                    key.startswith('title_source')):
                variant_titles.append((key, value))
            if key.startswith('contribution_end_date'):
                contribution_end_dates.append((key, value))
            if key.startswith('contribution_start_date'):
                contribution_start_dates.append((key, value))
            if key.startswith('given_name'):
                given_names.append((key, value))
            if key.startswith('person_authority_control_url'):
                person_authority_control_urls.append((key, value))
            if key.startswith('person_selected'):
                persons_selected.append((key, value))
            if key.startswith('role'):
                roles.append((key, value))
            if key.startswith('range_date_death'):
                range_date_deaths.append((key, value))
            if key.startswith('range_date_birth'):
                range_date_births.append((key, value))
            if key.startswith('surname'):
                surnames.append((key, value))
            if key.startswith('title_section1'):
                section_titles.append((key, value))

        sacred_or_secular = self._sacred_or_secular_to_bool(
            post_dict['_sacred_or_secular'])

        variant_titles_without_key = []
        for title in variant_titles:
            variant_titles_without_key.append(title[0])

        work = self._create_musical_work(variant_titles_without_key,
                                         sacred_or_secular)

        return HttpResponseRedirect('/musicalworks/')

    @staticmethod
    def _create_musical_work(variant_titles, sacred_or_secular) -> MusicalWork:
        work = MusicalWork(variant_titles=variant_titles,
                           _sacred_or_secular=sacred_or_secular)
        return work

    @staticmethod
    def _create_contribution(start_date, end_date, role, person,
                             certainty):
        date_range = DateRange(start_date, end_date)
        contribution = Contribution(_date=date_range,
                                    certainty_of_attribution=certainty,
                                    role=role,
                                    person=person)
        return contribution

    @staticmethod
    def _create_genre_type(name):
        return

    @staticmethod
    def _create_genre_style(name):
        return

    @staticmethod
    def _create_source(name):
        return

    @staticmethod
    def _create_person(name, surname, date_of_birth, date_of_death):
        return

    @staticmethod
    def _create_file(file_name):
        return

    @staticmethod
    def _create_section(section_name, ordering, musical_work):
        return

    @staticmethod
    def _create_instrument(name):
        return

    @staticmethod
    def _create_part(name, instrument, musical_work):
        return

    @staticmethod
    def _strip_prefix(prefix, string) -> Union[int, str]:
        if not string.startswith(prefix):
            return string
        else:
            return int(string[:len(string) - len(prefix)])

    @staticmethod
    def _sacred_or_secular_to_bool(_sacred_or_secular) -> Union[bool, None]:
        if (_sacred_or_secular == '1') or (_sacred_or_secular == 2):
            return None
        if _sacred_or_secular == '3':
            return True
        if _sacred_or_secular == '4':
            return False
