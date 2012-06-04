from django.conf.urls import patterns, include, url
from qdb.views import TopQuotesView, NewQuotesView, CreateQuoteView, \
    QuoteDetailView, QuoteEditView

urlpatterns = patterns('qdb.views',
    url(r'^$', TopQuotesView.as_view(), name='home'),
    url(r'^top$', TopQuotesView.as_view(), name='top'),
    url(r'^newest$', NewQuotesView.as_view(), name='newest'),
    url(r'^submit$', CreateQuoteView.as_view(), name='submit'),
    url(r'^quotes/(?P<pk>\d+)$', QuoteDetailView.as_view(), name='permalink'),
    url(r'^quotes/(?P<pk>\d+)/edit/$', QuoteEditView.as_view(), name='edit_quote'),

    url(r'^vote$', 'cast_vote', name='vote'),
)

