from __future__ import absolute_import
import json

from django.http import HttpResponse

from ...encoders import SerializableModelEncoder


class JsonResponseMixin(object):
    """
    Mixin to enrich your view class by providing a `render_to_json` and a
    `get_json` method. This makes it easier to quickly respond with json data.

    You can override the JSON encoder by setting the `json_encoder_class`
    attribute.
    """

    json_encoder_class = SerializableModelEncoder

    def get_json(self, data):
        return json.dumps(data, cls=self.json_encoder_class)

    def render_to_json(self, data, status=200):
        return HttpResponse(
            self.get_json(data),
            status=status,
            content_type='application/json'
        )
