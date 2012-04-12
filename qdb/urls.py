from django.conf.urls import patterns, include, url
from qdb.views import TopQuotesView, NewQuotesView, CreateQuoteView, \
    QuoteDetailView

urlpatterns = patterns('qdb.views',
    url(r'^$', TopQuotesView.as_view(), name='home'),
    url(r'^top$', TopQuotesView.as_view(), name='top'),
    url(r'^newest$', NewQuotesView.as_view(), name='newest'),
    url(r'^submit$', CreateQuoteView.as_view(), name='submit'),
    url(r'^quotes/(?P<pk>\d+)$', QuoteDetailView.as_view(), name='permalink'),

    url(r'^vote$', 'cast_vote', name='vote'),
)

