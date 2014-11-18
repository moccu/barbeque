from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet


class SerializableModelEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'serialize'):
            return obj.serialize()
        elif isinstance(obj, QuerySet):
            return list(obj)
        return DjangoJSONEncoder.default(self, obj)
