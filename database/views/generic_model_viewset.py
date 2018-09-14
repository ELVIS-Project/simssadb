from django.core.paginator import EmptyPage, InvalidPage, PageNotAnInteger, \
    Paginator
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, \
    TemplateHTMLRenderer
from rest_framework.response import Response

from database.utils.view_utils import *

PAGE_SIZE = 25


class GenericModelViewSet(viewsets.ModelViewSet):
    """Provide a Generic ModelViewSet that can return HTML or JSON.

    When using this, the subclass must override the `queryset`, `serializer`,
    `detail_fields` and `summary_fields` attributes.
    """

    # In the future we can add even more renderers to return things like XML
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer,
                        BrowsableAPIRenderer)
    detail_fields: Optional[List[str]] = None
    summary_fields: Optional[List[str]] = None
    badge_field: Optional[str] = None
    related_fields: Optional[List[Dict]] = None

    def list(self, request, *args, **kwargs) -> Response:
        """GETs a list of objects, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        paginator = Paginator(self.get_queryset(), PAGE_SIZE)
        page_num = request.GET.get('page', 1)
        try:
            page = paginator.page(page_num)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            page = paginator.page(1)
        object_list: List[CustomBaseModel] = page.object_list
        new_object_list = []

        for element in object_list:
            new_element = make_summary_dict(element,
                                            self.summary_fields,
                                            self.badge_field)
            new_object_list.append(new_element)

        page.object_list = new_object_list

        model_name = self.get_queryset().model.verbose_name_plural()
        if self.request.accepted_renderer.format == 'html':
            data = {
                'list':        page,
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

    def retrieve(self, request, *args, **kwargs) -> Response:
        """GETs an object, based on content negotiation

        :return: A list of objects in HTML or JSON format
        """
        response_object = self.get_object()
        if self.request.accepted_renderer.format == 'html':
            data = {
                'detail': make_detail_dict(instance=response_object,
                                           detail_fields=self.detail_fields,
                                           related_objects=self.related_fields)
                }
            response = Response(data, template_name='detail.html')
            return response
        else:
            data = self.get_serializer(instance=response_object).data
            return Response(data)
