from django.conf.urls import patterns, include, url
from qdb.views import TopQuotesView, NewQuotesView

urlpatterns = patterns('qdb.views',
    url(r'^$', TopQuotesView.as_view(), name='home'),
    url(r'^top$', TopQuotesView.as_view(), name='top'),
    url(r'^new$', NewQuotesView.as_view(), name='new'),

    url(r'^vote$', 'cast_vote', name='vote'),
)

