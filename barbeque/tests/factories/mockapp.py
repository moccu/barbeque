import factory

from barbeque.tests.resources.mockapp.models import ImageModel


class ImageModelFactory(factory.DjangoModelFactory):
    picture = factory.django.ImageField()

    class Meta:
        model = ImageModel
