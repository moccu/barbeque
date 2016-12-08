import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.template import RequestContext, TemplateDoesNotExist
from django.test.client import RequestFactory
from django.utils import translation


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Acrtivate language to ensure we get the translation right.
        translation.activate(settings.LANGUAGE_CODE)

        self.stdout.write('Rendering static templates..')
        templates = getattr(settings, 'BARBEQUE_STATIC_TEMPLATES', {})
        for filename, template_name in templates.items():
            self.handle_item(filename, template_name)

    def handle_item(self, filename, template_name):
        self.stdout.write(
            '> Rendering template "{0}" for "{1}"'.format(template_name, filename))

        content = self.render_template(template_name)
        if content is not None:
            self.write_file(filename, content)

    def render_template(self, template_name, context=None):
        template_context = {}
        template_context.update(getattr(settings, 'COMPRESS_OFFLINE_CONTEXT', {}))
        template_context.update(context or {})

        # We need a fake request to use the RequestContext, which is needed to
        # apply all context processors (for menus, etc.)
        request = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0].strip('.')).get('/')
        request.user = AnonymousUser()
        request.session = {}

        try:
            return render_to_string(template_name, RequestContext(request, template_context))
        except TemplateDoesNotExist:
            self.stdout.write(
                '- Template "{0}" does not exist!'.format(template_name))

    def write_file(self, name, content):
        path = os.path.join(settings.STATIC_ROOT, name)
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        self.stdout.write('- Writing file "{0}"'.format(path))
        with open(path, 'w+') as file_obj:
            file_obj.write(content)
