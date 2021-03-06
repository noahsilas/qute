from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeletionMixin
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseRedirect
from django.contrib import messages

from qdb.models import Quote, Vote
from qdb.forms import VoteForm, QuoteForm

def get_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', None) or \
           request.META['REMOTE_ADDR']


class QuoteListView(ListView):
    context_object_name = 'quotes'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
      context = {'show_permalink': True}
      context.update(
          super(QuoteListView, self).get_context_data(*args, **kwargs)
      )
      return context

    def get_queryset(self):
        return Quote.objects.active().with_scores()

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(QuoteListView, self).dispatch(*args, **kwargs)


class TopQuotesView(QuoteListView):
    def get_queryset(self):
        qs = super(TopQuotesView, self).get_queryset()
        return qs.order_by('-score')


class NewQuotesView(QuoteListView):
    def get_queryset(self):
        qs = super(NewQuotesView, self).get_queryset()
        return qs.order_by('-created_at')


class QuoteDetailView(DetailView, DeletionMixin):
    queryset = Quote.objects.active().with_scores()

    def get_success_url(self):
      return reverse('qdb:home')

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(QuoteDetailView, self).dispatch(*args, **kwargs)

    @method_decorator(permission_required('qdb.delete_quote'))
    def delete(self, request, *args, **kwargs):
      messages.success(request, 'Quote Deleted')
      self.object = self.get_object()
      self.object.hide()
      return HttpResponseRedirect(self.get_success_url())


class QuoteEditView(UpdateView):
    model = Quote
    form_class = QuoteForm
    queryset = Quote.objects.active().with_scores()

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(QuoteEditView, self).dispatch(*args, **kwargs)


def cast_vote(request):
    ip = get_ip(request)

    try:
        quote_id = request.POST['quote']
        day = now().replace(hour=0, minute=0, second=0, microsecond=0)
        vote = Vote.objects.active().get(
            ip=ip,
            quote_id=quote_id,
            created_at__gte=day
        )
    except Vote.DoesNotExist:
        vote = Vote(ip=ip)
    except Vote.MultipleObjectsReturned:
        return HttpResponseBadRequest()

    form = VoteForm(request.POST, instance=vote)
    if form.is_valid():
        vote = form.save()
        return HttpResponse(vote.quote.get_score())
    return HttpResponseBadRequest()


class CreateQuoteView(CreateView):
    model = Quote
    form_class = QuoteForm

    def get_success_url(self):
        return reverse('qdb:newest')

    def get_form_kwargs(self):
        kwargs = super(CreateQuoteView, self).get_form_kwargs()
        instance = self.model(ip=get_ip(self.request))
        kwargs.update({'instance': instance})
        return kwargs
