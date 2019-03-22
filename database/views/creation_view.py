from django.http import HttpResponseRedirect

from database.forms.creation_form import WorkInfoForm, ContributionForm
from database.forms.source_creation_form import SourceForm
from django.views.generic import FormView
from database.models import MusicalWork, Section, GenreAsInType,\
        GenreAsInStyle, Instrument, Part
from django.forms import formset_factory


class CreationView(FormView):

    template_name = 'creation_form.html'
    form_class = formset_factory(ContributionForm)

    def form_valid(self, form):
        data = form.data

        title = data.getlist('title')
        variant_titles = data.getlist('variant_title')
        variant_titles = title + variant_titles

        sacred_or_secular = data.getlist('sacred_or_secular')[0]
        if sacred_or_secular == 'True':
            s_or_s = True
        elif sacred_or_secular == 'False':
            s_or_s = False
        else:
            s_or_s = None

        work = MusicalWork.objects.create(variant_titles=variant_titles,
                                          _sacred_or_secular=s_or_s)

        genres_as_in_type = data.getlist('genre_as_in_type')
        genres_as_in_style = data.getlist('genre_as_in_style')

        styles = list(GenreAsInStyle.objects.filter(id__in=genres_as_in_style))
        types = list(GenreAsInType.objects.filter(id__in=genres_as_in_type))

        work.genres_as_in_style.add(*styles)
        work.genres_as_in_type.add(*types)

        work_id = str(work.id)
        return HttpResponseRedirect('/source/?work_id=' + work_id)


class FileCreationView(FormView):
    pass
