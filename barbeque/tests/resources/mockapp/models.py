from django.db import models


class MockModel(models.Model):
    pass


class RelatedMockModel(models.Model):
    parent = models.ForeignKey(MockModel, related_name='related_mock')
