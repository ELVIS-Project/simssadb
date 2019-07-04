from random import choices

from django import forms


class FacetSearchForm(forms.Form):
    def __init__(self, facets=None, *args, **kwargs):
        super(FacetSearchForm, self).__init__(*args, **kwargs)
        if facets:
            for key, facet in facets.items():
                choices = []
                for facet_value in facet.facet_values:
                    choices.append(
                        (
                            facet_value.pk,
                            "{0}({1})".format(
                                facet_value.display_name, facet_value.count
                            ),
                        )
                    )
                self.fields[key].choices = choices
                self.fields[key].label = facet.display_name

    widget = forms.CheckboxSelectMultiple(
        attrs={"class": "pre-scrollable", "style": "overflow:auto"}
    )
    q = forms.CharField(required=False, label="Search ")
    types = forms.MultipleChoiceField(widget=widget, required=False)
    styles = forms.MultipleChoiceField(widget=widget, required=False)
    composers = forms.MultipleChoiceField(widget=widget, required=False)
    instruments = forms.MultipleChoiceField(widget=widget, required=False)
    sacred = forms.MultipleChoiceField(widget=widget, required=False)
    file_formats = forms.MultipleChoiceField(widget=widget, required=False)
