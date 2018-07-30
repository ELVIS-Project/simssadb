from django import forms
from haystack.generic_views import FacetedSearchForm

from database.models.musical_work import MusicalWork


class NiceFacetForm(FacetedSearchForm):

    # TODO: clean this up
    def __init__(self, *args, **kwargs):
        super(NiceFacetForm, self).__init__(*args, **kwargs)
        self.selected_facets = ['places', 'dates', 'sym_formats',
                                'audio_formats',
                                'text_formats', 'image_formats', 'certainty',
                                'languages', 'religiosity', 'instruments',
                                'composers', 'types', 'styles']
        self.sqs = self.searchqueryset
        for facet in self.selected_facets:
            self.sqs = self.sqs.facet(facet)

        try:
            fields_dict = self.search().facet_counts()['fields']
            for field in fields_dict:
                if field == 'dates' or not fields_dict[field]:
                    continue
                choices = []
                for facet in fields_dict[field]:
                    text = facet[0]
                    count = facet[1]
                    if facet[1] == 0:
                        continue
                    if field == 'religiosity':
                        if facet[0] == 'true':
                            text = 'Sacred'
                        elif facet[0] == 'false':
                            text = 'Secular'
                        elif facet[0] == 'None':
                            text = 'Non Applicable'
                    if field == 'certainty':
                        if facet[0] == 'true':
                            text = 'Certain'
                        if facet[0] == 'false':
                            text = 'Uncertain'

                    choices.append((facet[0], "{0}({1})".format(text, count)))
                widget = forms.CheckboxSelectMultiple(attrs={
                    'class': 'pre-scrollable',
                    'style': 'overflow:auto'
                    })
                label = field
                if field == 'sym_formats':
                    label = 'Symbolic Music Format'
                if field == 'types':
                    label = 'Genre (Type)'
                if field == 'instruments':
                    label = 'Instrument or Voice'
                if field == 'composers':
                    label = 'Composer'
                if field == 'styles':
                    label = 'Genre (Style)'
                if field == 'religiosity':
                    label = 'Sacred/Secular'
                self.fields[field] = forms.MultipleChoiceField(choices=choices,
                                                               widget=widget,
                                                               required=False,
                                                               label=label)
        except KeyError:
            pass

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        self.sqs = self.sqs.models(MusicalWork)

        narrowing_query = ''
        for facet in self.selected_facets:
            chosen = self.data.getlist(facet)
            if chosen:
                narrow_subquery = ''
                for choice in chosen:
                    if narrow_subquery:
                        narrow_subquery += ' OR '
                    else:
                        narrow_subquery = ''
                    narrow_subquery += '""%s""' % self.sqs.query.clean(choice)
                narrowing_query += '%s_exact:"%s"' % (facet, narrow_subquery)

        self.sqs = self.sqs.narrow(narrowing_query)
        query = self.cleaned_data['q']
        self.sqs = self.sqs.filter(text__fuzzy=query)

        if self.load_all:
            self.sqs = self.sqs.load_all()

        return self.sqs
