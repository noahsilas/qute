from django.core.urlresolvers import resolve
from django.http import Http404
from django import template

register = template.Library()

@register.simple_tag
def active(request, view_name, active_class='active', inactive_class=''):
    if not hasattr(request, '_view_name'):
        try:
            urlconf = getattr(request, 'urlconf', None)
            match = resolve(request.path_info, urlconf=urlconf)
            request._view_name = match.view_name
        except Http404:
            request._view_name = None

    if request._view_name == view_name:
        return active_class
    return inactive_class

