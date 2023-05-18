import re
from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import FormView
from psycopg2.extras import DateRange
import datetime
from database.forms.forms import SourcesForm, ContributionMusicalWorkForm, \
    GenreStyleForm, GenreTypeForm, MusicalWorkForm, PartForm, PersonForm, \
    SectionForm, ResearchCorpusForm
from database.models import MusicalWork, ContributionMusicalWork, Person, \
    GeographicArea, GenreAsInType, GenreAsInStyle, Instrument, Part, Section, \
    SourceInstantiation, Source, File, Software, ResearchCorpus
from django.views.generic import CreateView


class CreateMusicalWorkViewCustom(FormView):
    template_name = 'musical_work_form.html'

    def get(self, request, *args, **kwargs):
        context = {
            'musical_work_form':          MusicalWorkForm,
            'style_form':                 GenreStyleForm,
            'type_form':                  GenreTypeForm,
            'person_form':                PersonForm,
            'contribution_form':          ContributionMusicalWorkForm,
            'part_form':                  PartForm,
           # 'collection_of_sources_form': SourcesForm,
            'sources_form':               SourcesForm,
            'section_form':               SectionForm
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_dict = request.POST
        variant_titles = []
        for key, value in post_dict.lists():
            if key.startswith('title') and not (
                    key.startswith('title_section') or
                    key.startswith('title_source')):
                variant_titles.append(value[0])

        sacred_or_secular = self._sacred_or_secular_to_bool(
            post_dict.get('_sacred_or_secular', 1))

        # Create work
        work = self._create_musical_work(variant_titles, sacred_or_secular)
        work.save()
        
        # Add styles and types
        styles = post_dict.getlist('genres_as_in_style')
        styles = list(map(lambda x: x.replace(';', ''), styles))
        style_ids = []
        for style in styles:
            match = re.match('[0-9]+', style)
            if match:
                style_ids.append(int(style))
                styles.remove(style)
        existing_styles = GenreAsInStyle.objects.filter(id__in=style_ids)
        new_styles = []
        for style in styles:
            new_style = GenreAsInStyle.objects.create(name=style)
            new_styles.append(new_style)
        for style in existing_styles:
            work.genres_as_in_style.add(style)
        for style in new_styles:
            work.genres_as_in_style.add(style)

        types = post_dict.getlist('genres_as_in_type')
        types = list(map(lambda x: x.replace(';', ''), types))
        type_ids = []
        for type_ in types:
            match = re.match('[0-9]+', type_)
            if match:
                type_ids.append(int(type_))
                types.remove(type_)
        existing_types = GenreAsInType.objects.filter(id__in=type_ids)
        new_types = []
        for type_ in types:
            new_type = GenreAsInType.objects.create(name=type_)
            new_types.append(new_type)
        for type_ in existing_types:
            work.genres_as_in_type.add(type_)
        for type_ in new_types:
            work.genres_as_in_type.add(type_)
        
        # Save
        work.save()
        
        # If there's an existing source, create an instantiation

        source_id = post_dict.get('source_selected', False)
        if source_id:
            source = Source.objects.get(pk=source_id)
            instantiation = self._create_source_instantiation(work, source)
            instantiation.save()
        else:
            source_title = post_dict.get('title_source_new', False)
            if not source_title:
                source_title = "PLACE HOLDER"
            start_date = post_dict.get('date_0', 0)
            end_date = post_dict.get('date_1', 0)
            portion = post_dict.get('portions', False)
            if not portion:
                portion = 'trivial portion' # what is portion what
            # collection = CollectionOfSources(title=source_title)
            # collection.save()
            source = Source(title=source_title,date_range_year_only=DateRange(start_date, end_date))
            source.save()
            instantiation = self._create_source_instantiation(work, source)
            instantiation.save()

        # Create contributions
        for index in range(1, 4):
            if post_dict.get('given_name' + str(index), False) or post_dict.get('person_selected' + str(index), False):
                contribution = self._parse_contribution(post_dict, index, work)
                contribution.save()

        # Create sections and parts
        instruments = post_dict.getlist('written_for')
        instruments = list(map(lambda x: x.replace(';', ''), instruments))
        instrument_ids = []
        for instrument in instruments:
            match = re.match('[0-9]+', instrument)
            if match:
                instrument_ids.append(int(instrument))
                instruments.remove(instrument)
        existing_instruments = Instrument.objects.filter(id__in=instrument_ids)
        new_instruments = []
        for instrument in instruments:
            new_instrument = Instrument.objects.create(name=instrument)
            new_instruments.append(new_instrument)

        for index in range(1, 4):
            section_title = post_dict.get('title_section' + str(index), False)
            if not section_title:
                if index == 1:
                    section_title = work.variant_titles[0]
                else:
                    continue
            section = self._create_section(section_title, work, index)
            section.save()
            for instrument in existing_instruments:
                part = self._create_part(instrument, section)
                part.save()
            for instrument in new_instruments:
                part = self._create_part(instrument, section)
                part.save()

        work_id = work.id
        for item in request.FILES:

            user_file = request.FILES[item]

            size = user_file.size

            file_type = user_file.content_type

            encoding_date = datetime.datetime.now()

            encoded_with = Encoder.objects.first()

            file = SymbolicMusicFile(file=user_file, manifests=instantiation,
                                     file_type=file_type, file_size=size,
                                     encoding_date=encoding_date,
                                     encoded_with=encoded_with)

            file.save()

        return HttpResponseRedirect('/musicalworks/' + str(work_id))

    def _parse_contribution(self, post_dict, index, work):
        person_id = post_dict.get('person_selected' + str(index), False)
        if person_id:
            person = Person.objects.get(pk=person_id)
        else:
            given_name = post_dict.get('given_name' + str(index), "")
            surname = post_dict.get('surname' + str(index), "")
            birth_start_date_text = post_dict.get('range_date_birth' + str(index) + '_0', False)
            if birth_start_date_text:
                start_date_birth = datetime.datetime.strptime(birth_start_date_text, '%Y').date()
            else:
                start_date_birth = None
            birth_end_date_text = post_dict.get('range_date_birth' + str(index) + '_0', False)
            if birth_end_date_text:
                end_date_birth = datetime.datetime.strptime(birth_end_date_text, '%Y').date()
            else:
                end_date_birth = None
            birth_date = DateRange(start_date_birth, end_date_birth)
            death_start_date_text = post_dict.get('range_date_death' + str(index) + '_0', False)
            if death_start_date_text:
                start_date_death = datetime.datetime.strptime(death_start_date_text, '%Y').date()
            else:
                start_date_death = None
            death_end_date_text = post_dict.get('range_date_death' + str(index) + '_0', False)
            if death_end_date_text:
                end_date_death = datetime.datetime.strptime(death_end_date_text, '%Y').date()
            else:
                end_date_death = None
            death_date = DateRange(start_date_death, end_date_death)
            person = self._create_person(given_name, surname, birth_date,
                                         death_date)
            person.save()
        location_id = post_dict.get('contribution_location' + str(index), False)
        if location_id:
            location = GeographicArea.objects.get(pk=location_id)
        else:
            location = None
        certainty_string = post_dict.get('certainty_of_attribution' + str(index), 'false')
        if certainty_string == 'true':
            certainty = True
        else:
            certainty = False
        start_date_birth = post_dict.get('contribution_start_date' + str(index), 0)
        end_date_birth = post_dict.get('contribution_end_date' + str(index), 0)
        role = post_dict.get('role' + str(index), "Composer")
        contribution = self._create_contribution(start_date_birth, end_date_birth, role,
                                                 person, certainty,
                                                 location, work)
        return contribution

    @staticmethod
    def _create_musical_work(variant_titles, sacred_or_secular) -> MusicalWork:
        work = MusicalWork(variant_titles=variant_titles,
                           _sacred_or_secular=sacred_or_secular)
        return work

    @staticmethod
    def _create_contribution(start_date, end_date, role, person,
                             certainty, location, work):
        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y').date()
        else:
            start_date = None
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y').date()
        else:
            end_date = None

        if start_date and end_date:
            date_range = DateRange(start_date, end_date)
        else:
            date_range = None

        if role == 'Author Of Text':
            role = 'author'
        role = role.upper()

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
    def _create_person(given_name, surname, date_of_birth, date_of_death):
        person = Person(given_name=given_name, surname=surname,
                        range_date_birth=date_of_birth, range_date_death=date_of_death)
        return person

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
    def _create_source_instantiation(musical_work, source):
        instantiation = SourceInstantiation(work=musical_work, source=source)
        return instantiation

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
        if _sacred_or_secular == '1':
            return None
        if _sacred_or_secular == '2':
            return True
        if _sacred_or_secular == '3':
            return False


class CreateResearchCorpus(CreateView):
    template_name = 'database/form.html'
    form_class = ResearchCorpusForm
    model = ResearchCorpus
