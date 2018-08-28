import warnings

from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, \
    Paginator
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, \
    TemplateHTMLRenderer
from rest_framework.response import Response

PAGE_SIZE = 25


class GenericModelViewSet(viewsets.ModelViewSet):
    """Provide a Generic ModelViewSet that can return HTML or JSON.

    When using this, the subclass must override the `queryset`, `serializer`,
    `detail_fields` and `summary_fields` attributes.
    """

    # In the future we can add even more renderers to return things like XML
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,
                        BrowsableAPIRenderer)
    detail_fields = []
    summary_fields = []
    # A list of tuples specifying the name of the field plus the names of the
    #  fields of the related objects that you wish to display
    related_fields = []

    @staticmethod
    def _make_fields_dict(instance, fields_list):
        fields_dict = {}

        for field in fields_list:
            key = field
            try:
                value = getattr(instance, field)
                if isinstance(value, QuerySet):
                    value = list(value)
                fields_dict.update({key: value})
            except AttributeError:
                warnings.simplefilter('always')
                warning_string = 'Did not find the field ' \
                                 + key + ' specified in fields_list'
                warnings.warn(warning_string)

        return fields_dict
    def get_model_name(self):
        return self.get_queryset().model._meta.verbose_name_plural

    def list(self, request, *args, **kwargs):
        """GETs a list of objects, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        paginator = Paginator(self.get_queryset(), PAGE_SIZE)
        page = request.GET.get('page', 1)
        try:
            list_ = paginator.page(page)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            list_ = paginator.page(1)
        model_name = self.get_model_name()
        if self.request.accepted_renderer.format == 'html':
            data = {
                'list':        list_,
                'model_name':  model_name,
                'model_count': self.get_queryset().count()
                }
            response = Response(data,
                                template_name='database/list.html')
            return response
        else:
            data = self.get_serializer(self.queryset, many=True,
                                       context={'request': request}).data
            return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """GETs an object, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        response_object = self.get_object()
        if self.request.accepted_renderer.format == 'html':
            data = {'detail': response_object.detail()}
            response = Response(data,
                                template_name='detail.html')
            return response
        else:
            data = self.get_serializer(instance=response_object).data
            return Response(data)
