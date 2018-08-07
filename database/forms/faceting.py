from django import forms
from haystack.generic_views import FacetedSearchForm

from database.models import SymbolicMusicFile


class NiceFacetForm(FacetedSearchForm):

    # TODO: clean this up
    def __init__(self, *args, **kwargs):
        super(NiceFacetForm, self).__init__(*args, **kwargs)
        self.selected_facets = ['religiosity', 'instruments',
                                'composers', 'types', 'styles',
                                'certainty']
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

        query = self.cleaned_data['q']
        self.sqs = self.sqs.models(SymbolicMusicFile).filter(text__fuzzy=query)

        kwargs = {}
        for facet in self.selected_facets:
            chosen = self.data.getlist(facet)
            if chosen:
                key = facet + '__in'
                key_value_pair = {key: chosen}
                kwargs.update(key_value_pair)
        self.sqs = self.sqs.filter(**kwargs)

        if self.load_all:
            self.sqs = self.sqs.load_all()

        return self.sqs
