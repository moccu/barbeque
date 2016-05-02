import logging
import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.template import RequestContext, TemplateDoesNotExist
from django.test.client import RequestFactory
from django.utils import translation


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @property
    def template_path(self):
        path = os.path.join(settings.STATIC_ROOT, 'errors')
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def write_file(self, name, content):
        path = os.path.join(self.template_path, '{name}.html'.format(name=name))
        logger.info('Writing file "{path}"'.format(path=path))

        with open(path, 'w+') as file_obj:
            file_obj.write(content)

    def render_template(self, template_name, context=None):
        template_context = {}
        template_context.update(getattr(settings, 'COMPRESS_OFFLINE_CONTEXT', {}))
        template_context.update(context or {})

        # We need a fake request to use the RequestContext, which is needed to
        # apply all context processors (for menus, etc.)
        request = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0].strip('.')).get('/')
        request.user = AnonymousUser()

        try:
            return render_to_string(template_name, RequestContext(request, template_context))
        except TemplateDoesNotExist as e:
            logger.error(
                'Template "{template}" does not exist!'.format(template=str(e)))

    def create_errorpage(self, error_code, template_name):
        logger.info(
            'Rendering template "{template_name}" for error code {error_code}'.format(
                template_name=template_name, error_code=error_code))

        content = self.render_template(template_name)
        if content is not None:
            self.write_file(error_code, content)

    def handle(self, *args, **options):
        # Acrtivate language to ensure we get the translation right.
        translation.activate(settings.LANGUAGE_CODE)

        logger.info('Creating error pages..')

        error_pages = getattr(settings, 'BARBEQUE_ERRORPAGES_MAP', {})
        for error_code, template_name in error_pages.items():
            self.create_errorpage(error_code, template_name)
