import os

from django.views.generic import TemplateView


class GenericTemplateView(TemplateView):
    def get_template_names(self):
        template_filename = '%s.html' % (self.kwargs['template'] or 'index')
        return [os.path.join('tests', template_filename)]
