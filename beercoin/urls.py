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
    url(r'^api/v1/beercoin/issue', 'beercoin.beercoin.views.issue_beercoin'),
	url(r'^api/v1/beercoin/redeem', 'beercoin.beercoin.views.redeem_beercoin'),
    url(r'^api/v1/beercoin/request/redeption', 'beercoin.beercoin.views.request_beercoin_redemption'),
    url(r'^api/v1/profile/$', 'beercoin.beercoin.views.list_profiles'),
    url(r'^api/v1/profile/(?P<profile_name>.*)$', 'beercoin.beercoin.views.get_profile'),
    url(r'^api/v1/check_login', 'beercoin.beercoin.views.check_login'),
    url(r'^activity/', include('actstream.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^0c308002f3737fbcb29960a2258cceeb.txt', TemplateView.as_view(template_name="empty.txt")),
    (r'^$', TemplateView.as_view(template_name="app.html")),
)

from django.conf import settings
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
