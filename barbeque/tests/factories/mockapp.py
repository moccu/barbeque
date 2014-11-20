import factory

from barbeque.tests.resources.mockapp.models import ImageModel


class ImageModelFactory(factory.DjangoModelFactory):
    picture = factory.django.ImageField(filename='test.jpg', width=400, height=400)

    class Meta:
        model = ImageModel
