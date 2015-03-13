from __future__ import absolute_import

import os

import factory
from filer.models import Image


class ImageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Image

    file = factory.django.ImageField(
        filename='image.jpg', color='orange', width=100, height=50)
    default_alt_text = factory.Sequence(lambda n: 'alt text {0}'.format(n))

    @classmethod
    def _after_postgeneration(cls, obj, *args, **kwargs):
        if obj.original_filename is None:
            obj.original_filename = os.path.basename(obj.file.name)
            obj.save()
