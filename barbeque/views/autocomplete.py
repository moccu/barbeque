from django.core.paginator import EmptyPage
from django.db.models import Q
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

from .mixins.json import JsonResponseMixin


class AutocompleteView(MultipleObjectMixin, JsonResponseMixin, View):
    search_field = None
    label_field = None
    value_field = None
    extra_fields = ()
    paginate_by = 10

    def get_field(self, obj, field_name):
        # Try on model.
        field = getattr(obj, field_name, None)
        if field is not None:
            if callable(field):
                return field()
            return field

        field = getattr(self, field_name)
        if callable(field):
            return field(obj)
        return field

    def filter_queryset(self):
        if self.request.GET.get('exact', ''):
            lookup = Q(**{'{0}__iexact'.format(
                self.search_field): self.request.GET['q']})
        else:
            lookup = Q(**{'{0}__icontains'.format(
                self.search_field): self.request.GET['q']})

        return self.get_queryset().filter(lookup)

    def get_result(self, obj):
        result = {
            'label': self.get_field(obj, self.label_field),
            'value': self.get_field(obj, self.value_field),
            'extra': {}
        }

        for field in self.extra_fields:
            result['extra'][field] = self.get_field(obj, field)

        return result

    def get(self, request, *args, **kwargs):
        if 'q' not in request.GET:
            return self.render_to_json(
                {'error': 'Missing "q" parameter.'}, status=400)

        self.object_list = self.filter_queryset()

        context = self.get_context_data()

        if context['page_obj']:
            pagination = {
                'current': context['page_obj'].number,
                'total': context['page_obj'].paginator.num_pages
            }

            try:
                pagination['next'] = context['page_obj'].next_page_number()
            except EmptyPage:
                pagination['next'] = None

            try:
                pagination['prev'] = context['page_obj'].previous_page_number()
            except EmptyPage:
                pagination['prev'] = None
        else:
            pagination = {
                'current': 1,
                'total': 1
            }

        return self.render_to_json({
            'q': self.request.GET['q'],
            'pages': pagination,
            'results': [self.get_result(obj) for obj in context['object_list']]
        })
