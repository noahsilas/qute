from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest

from qdb.models import Quote, Vote
from qdb.forms import VoteForm, QuoteForm

def get_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', None) or \
           request.META['REMOTE_ADDR']


class QuoteListView(ListView):
    context_object_name = 'quotes'
    paginate_by = 10

    def get_queryset(self):
        return Quote.objects.active().with_scores()


class TopQuotesView(QuoteListView):
    def get_queryset(self):
        qs = super(TopQuotesView, self).get_queryset()
        return qs.order_by('-score')


class NewQuotesView(QuoteListView):
    def get_queryset(self):
        qs = super(NewQuotesView, self).get_queryset()
        return qs.order_by('-created_at')


def cast_vote(request):
    vote = Vote(ip=get_ip(request))
    form = VoteForm(request.POST, instance=vote)
    if form.is_valid():
        vote = form.save()
        return HttpResponse()
    return HttpResponseBadRequest()


class CreateQuoteView(CreateView):
    model = Quote
    form_class = QuoteForm

    def get_success_url(self):
        return reverse('qdb:new')

    def get_form_kwargs(self):
        kwargs = super(CreateQuoteView, self).get_form_kwargs()
        instance = self.model(ip=get_ip(self.request))
        kwargs.update({'instance': instance})
        return kwargs
