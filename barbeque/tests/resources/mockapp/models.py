from django.db import models


class MockModel(models.Model):
    pass


class RelatedMockModel(models.Model):
    parent = models.ForeignKey(MockModel, related_name='related_mock')
    value = models.CharField(max_length=256, default='', blank=True)


class DummyModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
