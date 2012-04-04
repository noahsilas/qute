from django.conf.urls import patterns, include, url

urlpatterns = patterns('qdb.views',
    url(r'^$', 'top_quotes', name='home'),
    url(r'^top$', 'top_quotes', name='top'),
    url(r'^new$', 'new_quotes', name='new'),

    url(r'^vote$', 'cast_vote', name='vote'),
)

