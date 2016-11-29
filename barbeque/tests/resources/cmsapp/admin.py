from cms.extensions import TitleExtensionAdmin
from django.contrib import admin

from .models import ExtensionModel


admin.site.register(ExtensionModel, TitleExtensionAdmin)
