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
        self.queryset = self.get_queryset()
        if self.request.accepted_renderer.format == 'html':
            data = {'detail': response_object.detail()}
            response = Response(data,
                                template_name='detail.html')
            return response
        else:
            data = self.get_serializer(instance=response_object).data
            return Response(data)
