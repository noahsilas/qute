from django.conf.urls import patterns, include, url
from qdb.views import TopQuotesView, NewQuotesView, CreateQuoteView

urlpatterns = patterns('qdb.views',
    url(r'^$', TopQuotesView.as_view(), name='home'),
    url(r'^top$', TopQuotesView.as_view(), name='top'),
    url(r'^new$', NewQuotesView.as_view(), name='new'),
    url(r'^submit$', CreateQuoteView.as_view(), name='submit'),

    url(r'^vote$', 'cast_vote', name='vote'),
)

