from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField()
    preview = models.ImageField(upload_to='preview/', auto_created=True)

    def __str__(self):
        return self.name
