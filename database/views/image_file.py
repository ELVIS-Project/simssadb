from database.models.image_file import ImageFile
from database.serializers import ImageFileSerializer
from database.views.generic_model_viewset import GenericModelViewSet


class ImageFileViewSet(GenericModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    summary_fields = ['file_type', 'manifests']
    detail_fields = ['encoded_with',
                     'encoding_date',
                     'file_size',
                     'file_type',
                     'extra_metadata',
                     'validated_by',
                     'version',
                     'musical_work',
                     'sections',
                     'parts',
                     'manifests',
                     'file']
