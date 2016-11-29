from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^non-cms/', TemplateView.as_view(template_name='empty_template.html')),
    url(r'', include('cms.urls')),
]
