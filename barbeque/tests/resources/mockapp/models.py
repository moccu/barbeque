from django.db import models

from barbeque.db.mixins import ProcessableFileMixin


class MockModel(models.Model):
    pass


class RelatedMockModel(models.Model):
    parent = models.ForeignKey(MockModel, related_name='related_mock')
    value = models.CharField(max_length=256, default='', blank=True)


class ImageModel(models.Model, ProcessableFileMixin):
    picture = models.ImageField(upload_to='uploads')
