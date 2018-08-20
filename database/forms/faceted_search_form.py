from django import forms
from haystack.forms import SearchForm


class FacetedSearchForm(SearchForm):

    def __init__(self, selected_facets, search_queryset, *args,
                 **kwargs):
        super(FacetedSearchForm, self).__init__(*args, **kwargs)
        self.selected_facets = selected_facets
        self.sqs = search_queryset
        for facet in self.selected_facets:
            self.sqs = self.sqs.facet(facet)

        try:
            fields_dict = self.sqs.facet_counts()['fields']
            for field in fields_dict:
                if field == 'dates' or not fields_dict[field]:
                    continue
                choices = []

                # TODO: handle this better
                for facet in fields_dict[field]:
                    text = facet[0]
                    count = facet[1]
                    if facet[1] == 0:
                        continue
                    if field == 'sacred_or_secular':
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

                self.fields[field] = forms.MultipleChoiceField(choices=choices,
                                                               widget=widget,
                                                               required=False,
                                                               label=field)
        except KeyError:
            pass
