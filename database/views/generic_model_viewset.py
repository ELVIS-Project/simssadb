from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, \
    TemplateHTMLRenderer
from rest_framework.response import Response


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
        if self.get_queryset is not None:
            if len(self.queryset) > 0:
                return self.get_queryset()[0].__class__.__name__.lower()
            else:
                return 'noresults'
        else:
            raise ValueError('Did not provide a queryset!')

    def get_detail_template_name(self):
        """Get the detail_template_name for this view

        It assumes that the detail template is named `<modelname>_detail.html`
        """
        return self.get_base_name() + '_detail.html'

    def get_list_template_name(self):
        """Get the list_template_name for this view

        It assumes that the list template is named `<modelname>_list.html`
        """
        return self.get_base_name() + '_list.html'


    def list(self, request, *args, **kwargs):
        """GETs a list of objects, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        context_variable = self.get_base_name() + '_list'
        self.queryset = self.get_queryset()
        if self.request.accepted_renderer.format == 'html':
            data = {context_variable: self.get_queryset()}
            response = Response(data,
                                template_name=self.get_list_template_name())
            return response
        else:
            data = self.get_serializer(self.queryset, many=True,
                                       context={'request': request}).data
            return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """GETs an object, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        self.object = self.get_object()
        context_variable = self.get_base_name()
        self.queryset = self.get_queryset()
        if self.request.accepted_renderer.format == 'html':
            data = {context_variable: self.object}
            response = Response(data,
                                template_name=self.get_detail_template_name())
            return response
        else:
            data = self.get_serializer(instance=self.object).data
            return Response(data)
