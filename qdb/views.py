from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseBadRequest

from qdb.models import Quote, Vote
from qdb.forms import VoteForm

def get_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', None) or \
           request.META['REMOTE_ADDR']


@ensure_csrf_cookie
def top_quotes(request):
    page = request.GET.get('page', 1)
    page -= 1   # convert page to zero indexing
    page_size = 10

    quotes = Quote.objects.active(
                         ).with_scores(
                         ).order_by('-score'
                         )[page * page_size:(page + 1)*page_size]
    context = {
        'quotes': quotes,
    }
    return render(request, 'qdb/quotes.html', context)


@ensure_csrf_cookie
def new_quotes(request):
    page = request.GET.get('page', 1)
    page -= 1   # convert page to zero indexing
    page_size = 10

    quotes = Quote.objects.active(
                         ).with_scores(
                         ).order_by('-created_at'
                         )[page * page_size:(page + 1)*page_size]
    context = {
        'quotes': quotes,
    }
    return render(request, 'qdb/quotes.html', context)


def cast_vote(request):
    vote = Vote(ip=get_ip(request))
    form = VoteForm(request.POST, instance=vote)
    if form.is_valid():
        vote = form.save()
        return HttpResponse()
    return HttpResponseBadRequest()
