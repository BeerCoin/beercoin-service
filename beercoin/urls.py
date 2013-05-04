from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'beercoin.views.home', name='home'),
    # url(r'^beercoin/', include('beercoin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/v1/check_login', 'beercoin.beercoin.views.check_login'),
    url(r'^activity/', include('actstream.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', TemplateView.as_view(template_name="app.html")),
)
