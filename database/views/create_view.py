from typing import Union

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import FormView
from psycopg2.extras import DateRange
import datetime
from database.forms.forms import CollectionOfSourcesForm, ContributionForm, \
    GenreStyleForm, GenreTypeForm, MusicalWorkForm, PartForm, PersonForm, \
    SectionForm, SourcesForm
from database.models import MusicalWork, Contribution, Person, \
    GeographicArea, GenreAsInType, GenreAsInStyle, Instrument, Part, Section, \
    SourceInstantiation, Source, SymbolicMusicFile, Encoder


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

    def post(self, request, *args, **kwargs):
        post_dict = request.POST
        variant_titles = []
        for key, value in post_dict.lists():
            if key.startswith('title') and not (
                    key.startswith('title_section') or
                    key.startswith('title_source')):
                variant_titles.append(value[0])

        sacred_or_secular = self._sacred_or_secular_to_bool(
            post_dict['_sacred_or_secular'])

        # Create work
        work = self._create_musical_work(variant_titles, sacred_or_secular)
        work.save()
        
        # Add styles and types
        style_ids = post_dict.getlist('genres_as_in_style')
        styles = GenreAsInStyle.objects.filter(id__in=style_ids)
        for style in styles:
            work.genres_as_in_style.add(style)

        type_ids = post_dict.getlist('genres_as_in_type')
        types = GenreAsInType.objects.filter(id__in=type_ids)
        for type_ in types:
            work.genres_as_in_type.add(type_)
        # Save
        work.save()
        
        # If there's an existing source, create an instantiation
        source_id = post_dict['source_selected']
        if source_id:
            source = Source.objects.get(pk=source_id)
            instantiation = self._create_source_instantiation(work, source)
            instantiation.save()
        else:
            # TODO: write logic to create a new source
            pass

        # Create contributions
        for index in range(1, 4):
            contribution = self._parse_contribution(post_dict, index, work)
            contribution.save()

        # Create sections and parts
        instrument_ids = post_dict.getlist('written_for')
        instruments = Instrument.objects.filter(id__in=instrument_ids)

        for index in range(1, 4):
            try:
                section_title = post_dict['title_section' + str(index)]
            except MultiValueDictKeyError:
                continue
            section = self._create_section(section_title, work, index)
            section.save()
            for instrument in instruments:
                part = self._create_part(instrument, section)
                part.save()

        work_id = work.id

        print(request.FILES)

        user_file = request.FILES['file1']

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
