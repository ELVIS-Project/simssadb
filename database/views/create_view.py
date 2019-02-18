import pprint
from pprint import pprint
from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from psycopg2.extras import DateRange
import datetime
from database.forms.forms import CollectionOfSourcesForm, ContributionForm, \
    GenreStyleForm, GenreTypeForm, MusicalWorkForm, PartForm, PersonForm, \
    SectionForm, SourcesForm
from database.models import MusicalWork, Contribution, Person, \
    GeographicArea, GenreAsInType, GenreAsInStyle, Instrument, Part, Section, \
    SourceInstantiation, Source, SymbolicMusicFile


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
        certainties_of_attribution = []
        locations = []
        orderings = []
        sources = []

        for key, value in post_dict.lists():
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
            if key.startswith('certainty_of_attribution'):
                certainties_of_attribution.append((key, value))
            if key.startswith('contribution_location'):
                locations.append((key, value))
            if key.startswith('ordering'):
                orderings.append((key, value))
            if key.startswith('source_selected'):
                sources.append((key, value))

        sacred_or_secular = self._sacred_or_secular_to_bool(
            post_dict['_sacred_or_secular'])

        titles = variant_titles[0][1]

        work = self._create_musical_work(titles,
                                         sacred_or_secular)
        work.save()

        source_id = sources[0][1][0]
        source = Source.objects.get(pk=source_id)

        instantiation = SourceInstantiation(work=work, source=source)
        instantiation.save()

        # TODO: handle this better, right now it might crash b/c of indices
        start_date = contribution_start_dates[0][1][0]
        end_date = contribution_end_dates[0][1][0]
        role = roles[0][1][0]
        person_id = persons_selected[0][1][0]
        person = Person.objects.get(pk=person_id)
        certainty_string = certainties_of_attribution[0][1][0]
        location_id = locations[0][1][0]
        location = GeographicArea.objects.get(pk=location_id)
        if certainty_string == 'true':
            certainty = True
        else:
            certainty = False

        contribution = self._create_contribution(start_date, end_date,
                                                 role, person, certainty,
                                                 location, work)
        contribution.save()

        type_ids = post_dict.getlist('genres_as_in_type')
        types = GenreAsInType.objects.filter(id__in=type_ids)

        for type_ in types:
            work.genres_as_in_type.add(type_)

        style_ids = post_dict.getlist('genres_as_in_style')
        styles = GenreAsInStyle.objects.filter(id__in=style_ids)

        for style in styles:
            work.genres_as_in_style.add(style)
        work.save()

        instrument_ids = post_dict.getlist('written_for')
        instruments = Instrument.objects.filter(id__in=instrument_ids)

        section_title = section_titles[0][1][0]
        ordering = int(orderings[0][1][0])
        section = self._create_section(section_title, work, ordering)
        section.save()

        for instrument in instruments:
            part = self._create_part(instrument, section)
            part.save()

        print(request.FILES)

        # user_file = request.FILES['file1']

        # file = SymbolicMusicFile(file=user_file, manifests=instantiation)

        work_id = work.id

        return HttpResponseRedirect('/musicalworks/' + str(work_id))

    @staticmethod
    def _create_musical_work(variant_titles, sacred_or_secular) -> MusicalWork:
        work = MusicalWork(variant_titles=variant_titles,
                           _sacred_or_secular=sacred_or_secular)
        return work

    @staticmethod
    def _create_contribution(start_date, end_date, role, person,
                             certainty, location, work):

        start_date = datetime.datetime.strptime(start_date, '%Y').date()
        end_date = datetime.datetime.strptime(end_date, '%Y').date()

        if role == 'Author Of Text':
            role = 'author'
        role = role.upper()
        date_range = DateRange(start_date, end_date)
        contribution = Contribution(_date=date_range,
                                    certainty_of_attribution=certainty,
                                    role=role,
                                    person=person,
                                    location=location,
                                    contributed_to_work=work)
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
    def _create_section(title, musical_work, ordering):
        section = Section(title=title,
                          musical_work=musical_work,
                          ordering=ordering)
        return section

    @staticmethod
    def _create_instrument(name):
        return

    @staticmethod
    def _create_part(instrument, section):
        part = Part(written_for=instrument, section=section)
        return part

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
