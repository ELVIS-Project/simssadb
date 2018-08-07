from django.shortcuts import render
from django.views.generic import FormView

from database.forms.content_search import ContentSearchForm


class ContentSearch(FormView):
    form_class = ContentSearchForm
    template_name = 'search/content_search.html'

    def get(self, request, *args, **kwargs):
        if not request.GET:
            return render(request, self.template_name, {'form':
                                                        self.form_class()})
        form = self.get_form()
        files = []
        for key, value in request.GET.lists():
            min_value, max_value = value[0].split(',')
            files.extend(form.search(key, min_value, max_value))
        context = {
            'list': files,
            'model_name': 'Files',
            'model_count': len(files),
            'form': self.form_class()
            }
        return render(request, self.template_name, context)
