============
JSON Encoder
============

A json encoder extension based on :class:`~django.core.serializers.json.DjangoJSONEncoder`
that supports manualize serialization of objects.

Given the following model:

.. code-block:: python

    from django.forms.models import model_to_dict

    class Recipe(models.Model):
        url = models.URLField(max_length=2048, blank=True)
        title = models.CharField(max_length=80)
        author = models.ForeignKey('accounts.User')
        description = models.TextField(blank=True)

        def serialize(self):
            data = model_to_dict(self, fields=('url', 'title', 'description'))
            data['author'] = self.author.pk
            return data


Now we're able to serialize all instances of ``Recipe`` to json.


.. code-block:: pycon

    >>> import json
    >>> from barbeque.encoders import SerializableModelEncoder

    >>> recipes = Recipe.objects.all()
    >>> print(json.dumps(recipes, cls=SerializableModelEncoder))
    '[{"url": "", "title": "Chocolate Cookies", "author": 28}]'
