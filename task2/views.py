import io

from django.core.files import File
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image as Img

from .models import Image
from .serializers import ImageSerializer


MAX_SIZE = 1024 * 1024 * 10


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'all items': '/api/',
        'get all images': 'GET /api/images/',
        'get image by id': 'GET /api/images/id/',
        'add new image': 'POST /api/images/',
        'delete image': 'DELETE /api/images/id/',
        'conversion task see example': 'GET /api/currency/',
        'conversion task': 'POST /api/currency/',
    }

    return Response(api_urls)


class ImageAPIView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        if request.data['image'].size > MAX_SIZE:
            return Response({"error": "File size exceeded, maximum size allowed is 10MB."},
                            status=status.HTTP_400_BAD_REQUEST)

        img = Image.objects.create(name=request.data['name'], image=request.data['image'])
        img.save()

        self.make_preview_image(img)
        img.image.close()

        serializer = self.get_serializer(img)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def make_preview_image(image: Image):
        preview_io = io.BytesIO()

        with Img.open(image.image) as pil_image:
            pil_image = pil_image.resize((100, 100))
            pil_image.save(preview_io, 'png')

        image.preview.save(f'{image.name}.png', File(preview_io))
        preview_io.close()
