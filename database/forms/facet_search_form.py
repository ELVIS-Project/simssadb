from random import choices
from typing import List, Optional
from django import forms
from database.views.facets import Facet


class FacetSearchForm(forms.Form):
    def __init__(
        self, facets: Optional[List[Facet]], work_ids: List[int], *args, **kwargs
    ) -> None:
        super(FacetSearchForm, self).__init__(*args, **kwargs)
        if facets:
            for facet in facets:
                choices = []
                facet.facet_values = facet.make_facet_values(work_ids)
                for facet_value in facet.facet_values:
                    if facet_value is not None:
                        choices.append(
                            (
                                facet_value.pk,
                                "{0}({1})".format(
                                    facet_value.display_name, facet_value.count
                                ),
                            )
                        )
                self.fields[facet.name].choices = choices
                self.fields[facet.name].label = facet.display_name

    widget = forms.CheckboxSelectMultiple(
        attrs={
            "class": "pre-scrollable",
            "style": "overflow:auto; ul:list-group; li:list-group-item;",
        }
    )
    search_widget = forms.TextInput(
        attrs={
            "class": "form-control-sm form-control"
        }
    )
    widget.template_name = "widgets/checkbox_select.html"
    q = forms.CharField(required=False, label="Search", widget=search_widget)
    types = forms.MultipleChoiceField(widget=widget, required=False)
    styles = forms.MultipleChoiceField(widget=widget, required=False)
    composers = forms.MultipleChoiceField(widget=widget, required=False)
    instruments = forms.MultipleChoiceField(widget=widget, required=False)
    sacred = forms.MultipleChoiceField(widget=widget, required=False)
    file_formats = forms.MultipleChoiceField(widget=widget, required=False)
