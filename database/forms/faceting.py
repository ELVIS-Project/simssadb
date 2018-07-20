from haystack.forms import FacetedSearchForm
from django import forms
from database.models import MusicalWork


class NiceFacetForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        super(NiceFacetForm, self).__init__(*args, **kwargs)
        try:
            fields_dict = self.search().facet_counts()['fields']
            print(fields_dict)
            for field in fields_dict:
                if field == 'dates' or not fields_dict[field]:
                    continue
                choices = []
                for facet in fields_dict[field]:
                    if facet[1] == 0:
                        continue
                    choices.append((facet[0], "{0}({1})".format(facet[0], facet[1])))
                custom_widget = forms.CheckboxSelectMultiple(attrs={'class': 'pre-scrollable',
                                                                    'style': 'overflow:auto'})
                label = 'Filter by ' + field
                self.fields[field] = forms.MultipleChoiceField(choices=choices,
                                                               widget=custom_widget,
                                                               required=False, label=label)
        except KeyError:
            pass

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get("q"):
            return self.no_query_found()

        query = self.cleaned_data['q']
        sqs = self.searchqueryset.models(MusicalWork).filter(text__fuzzy=query)

        if self.load_all:
            print(sqs.facet_counts())
            sqs = sqs.load_all()

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                sqs = sqs.narrow('%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs
