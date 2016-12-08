from django.conf import settings
from django.utils import translation

from .render_static_templates import Command as RenderCommand


class Command(RenderCommand):

    def handle(self, *args, **options):
        # Acrtivate language to ensure we get the translation right.
        translation.activate(settings.LANGUAGE_CODE)

        self.stdout.write('Creating error pages..')

        error_pages = getattr(settings, 'BARBEQUE_ERRORPAGES_MAP', {})
        for error_code, template_name in error_pages.items():
            self.handle_item('errors/{0}.html'.format(error_code), template_name)
