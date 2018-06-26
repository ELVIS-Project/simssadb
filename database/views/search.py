from haystack.query import SearchQuerySet
from haystack.generic_views import SearchView
from django.apps import apps


class GeneralSearch(SearchView):
    template_name = 'search/general-search.html'

    # TODO: Make this more robust in terms of getting parameters from the URL
    def get_queryset(self):
        queryset = super(GeneralSearch, self).get_queryset()
        if self.request.method == 'GET':
            params = self.request.GET
            if params.getlist('q') and not params.getlist('models',
                                                          default=False):
                queryset = SearchQuerySet().filter(text__fuzzy=params['q'])
            if params.getlist('models'):
                models = []
                for item in params.getlist('models'):
                    app_label, model_name = item.split('.')
                    model = apps.get_model(app_label=app_label,
                                           model_name=model_name)
                    models.append(model)
                queryset = SearchQuerySet().models(*models).filter(
                        text__fuzzy=params['q'])
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(GeneralSearch, self).get_context_data(*args, **kwargs)
        context['size'] = len(self.get_queryset())
        context['object_list'] = self.get_queryset().load_all()
        return context
