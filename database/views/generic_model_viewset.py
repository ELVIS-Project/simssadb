from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, \
    TemplateHTMLRenderer
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

PAGE_SIZE = 25


class GenericModelViewSet(viewsets.ModelViewSet):
    """Provide a Generic ModelViewSet that can return HTML or JSON

    When using this, the subclass must override the `queryset` and `serializer`
    attributes
    """

    # In the future we can add even more renderers to return things like XML
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,
                        BrowsableAPIRenderer)

    def get_base_name(self):
        """Get the base_name that will be used in this view

        The base_name will be used to construct the template names and the
        context variable names
        """
        base_name = self.get_queryset().model.__name__.lower()
        if base_name:
            return base_name
        else:
            raise ValueError('Did not provide a queryset!')

    def get_detail_template_name(self):
        """Get the detail_template_name for this view

        It assumes that the detail template is named `<modelname>_detail.html`
        """
        return self.get_base_name() + '_detail.html'

    def get_model_name(self):
        try:
            return self.get_queryset().model.verbose_name_plural
        except AttributeError:
            return self.get_base_name() + 's'

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
            data = {'list': list_,
                    'model_name': model_name,
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
        context_variable = self.get_base_name()
        self.queryset = self.get_queryset()
        if self.request.accepted_renderer.format == 'html':
            data = {context_variable: response_object}
            response = Response(data,
                                template_name=self.get_detail_template_name())
            return response
        else:
            data = self.get_serializer(instance=response_object).data
            return Response(data)
