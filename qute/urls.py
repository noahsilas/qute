from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from qdb.views import TopQuotesView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qute.views.home', name='home'),
    # url(r'^qute/', include('qute.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TopQuotesView.as_view(), name='home'),
    url(r'^qdb/', include('qdb.urls', namespace='qdb')),
    url(r'^about$', direct_to_template, {'template':'about.html'}, name='about'),
)

urlpatterns += staticfiles_urlpatterns()
