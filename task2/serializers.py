from rest_framework import serializers
from task2.models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_type = serializers.SerializerMethodField()
    preview = serializers.ImageField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'name', 'image_type', 'preview', 'image')

    def get_image_type(self, obj):
        return obj.image.__str__().split('.')[-1]
